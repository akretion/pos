/******************************************************************************
    Point Of Sale - POS Order Reprint for Odoo
    Copyright (C) 2015-Today Akretion (http://www.akretion.com)
    @author Sylvain Calador <sylvain.calador@akretion.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/

openerp.pos_order_reprint = function(instance) {
    module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    var push_order_original = module.PosModel.prototype.push_order;
    module.PosModel = module.PosModel.extend({

        push_order: function(order) {
            if (_.isUndefined(order)) {
                return push_order_original.call(this, order);
            }

            var receipt = order.export_for_printing();
            order.xml_sale_receipt = QWeb.render('XmlReceipt', {
                receipt: receipt, widget: this.pos_widget,
            });
            return push_order_original.call(this, order);
        }
    });

    module.ProductCategoriesWidget.include({

        init: function (parent, options) {
            this._super(parent, options);
        },

        renderElement: function () {
            var self = this;
            this._super();
            $('#all_orders').click(function () {
                 self.pos_widget.screen_selector.set_current_screen('orderlist');
            });
        },
    });

    module.PosWidget = module.PosWidget.extend({
        build_widgets: function() {
            this._super();

            this.orderlist_screen = new module.OrderListScreenWidget(this, {});
            this.orderlist_screen.appendTo(this.$('.screens'));
            this.orderlist_screen.hide();

            this.screen_selector.screen_set['orderlist'] =
                this.orderlist_screen;
        },
    });

    var export_as_JSON_original = module.Order.prototype.export_as_JSON;
    module.Order = module.Order.extend({

        export_as_JSON: function() {
            var res = export_as_JSON_original.call(this);
            var order = this.pos.get('selectedOrder');
            res.xml_sale_receipt = order.xml_sale_receipt;
            return res;
        }

    });

    module.OrderListScreenWidget = module.ScreenWidget.extend({
        template: 'OrderListScreenWidget',
        next_screen: 'orderlist',
        show_leftpane: false,
        model: 'pos.order',

        init: function(parent, options){
            this._super(parent, options);
        },

        start: function() {
            var self = this;
            this._super();
            this.$el.find('span.button.back').click(function(){
                var ss = self.pos.pos_widget.screen_selector;
                ss.set_current_screen('products');
            });

            var search_timeout = null;

            this.$('.searchbox input').on('keyup',function(event){
                clearTimeout(search_timeout);

                var query = this.value;

                search_timeout = setTimeout(function(){
                    self.perform_search(query);
                },70);

            });

            this.$('.searchbox .search-clear').click(function(){
                self.clear_search();
            });

        },

        load_orders: function(query) {
            var self = this;
            var orderModel = new instance.web.Model(this.model);
            return orderModel.call('search_read_orders_reprint', [query || ''])
            .then(function (result) {
                self.render_list(result);
            }).fail(function (error, event){
                if (error.code === 200) {
                    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup(
                        'error-traceback', {
                            message: error.data.message,
                            comment: error.data.debug
                        }
                    );
                }
                console.error('Failed to load pos orders:', query);
                self.pos_widget.screen_selector.show_popup('error',{
                    message: 'Connection error',
                    comment: 'Can not execute this action because the POS \
                        is currently offline',
                });
                event.preventDefault();
            });
        },

        show: function() {
            this._super();
            var ss = this.pos.pos_widget.screen_selector;
            if (ss.get_current_screen() =='orderlist') {
                this.load_orders();
            }
        },

        render_list: function(orders) {
            var self = this;
            var contents = this.$el[0].querySelector('.order-list-contents');
            contents.innerHTML = "";
            for (var i = 0, len = orders.length; i < len; i++){
                var order = orders[i];
                var orderline_html = QWeb.render('OrderListLine',
                    {widget: this, order:order, moment: moment});
                var orderline = document.createElement('tbody');
                orderline.innerHTML = orderline_html;
                orderline = orderline.childNodes[1];
                orderline.querySelector('button').addEventListener('click',
                    function(){
                        var order_id = parseInt(this.dataset['orderId']);
                        self.print_order(order_id);
                    }
                );

                contents.appendChild(orderline);
            }
        },

        perform_search: function(query) {
            this.load_orders(query)
        },

        clear_search: function() {
            this.load_orders();
            this.$('.searchbox input')[0].value = '';
            this.$('.searchbox input').focus();
        },

        // to override if necessary
        add_product_attribute: function(product, key, orderline){
            return product;
        },

        print_order: function(order_id) {
            var self = this;
            var orderModel = new instance.web.Model(this.model);
            return orderModel.call('load_xml_sale_receipt', [order_id])
            .then(function (result) {
                var result = result[0];

                if(self.pos.config.iface_print_via_proxy){
                    var xml = result['xml_sale_receipt'];
                    console.debug('receipt xml', xml);
                    self.pos.proxy.print_receipt(xml);
                } else {
                    console.error('Unable to print, please check your POS configuration');
                }

                self.pos_widget.screen_selector.set_current_screen(self.next_screen);

            }).fail(function (error, event){
                if (error.code === 200) {
                    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup(
                        'error-traceback', {
                            message: error.data.message,
                            comment: error.data.debug
                        });
                }
                console.error('Failed to load order for printing:', order_id);
                self.pos_widget.screen_selector.show_popup('error',{
                    message: 'Connection error',
                    comment: 'Can not execute this action because the POS \
                        is currently offline',
                });
                event.preventDefault();
            });

        },

    });

}
