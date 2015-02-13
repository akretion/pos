/******************************************************************************
 * Point Of Sale - Product Template module for Odoo
 * Copyright (C) 2014-Today Akretion (http://www.akretion.com)
 * @author Sylvain Calador (sylvain.calador@akretion.com)
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *****************************************************************************/

openerp.pos_sale_order_load = function(instance, local) {
    module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    var round_pr = instance.web.round_precision;

    var export_as_JSON_original = module.Order.prototype.export_as_JSON;
    module.Order = module.Order.extend({

        export_as_JSON: function() {
            var res = export_as_JSON_original.call(this);
            res.order_id = this.get_order_id();
            return res;
        },

    });

    module.OrderListScreenWidget = module.OrderListScreenWidget.extend({
        model: 'sale.order',

        init: function(parent, options) {
            this._super(parent, options);
        },
    });

}
