# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-TODAY Akretion (<http://www.akretion.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _prepare_sale_order_vals(self, cr, uid, ui_order, context=None):
        context = context or {}
        res = super(PosOrder, self)._prepare_sale_order_vals(
            cr, uid, ui_order, context=context)
        if 'order_id' in ui_order:
            res['order_id'] = ui_order['order_id']
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if 'order_id' in vals:
            order = self.browse(vals['order_id'])
            vals['order_line'] = [(5, 0)] + vals['order_line']
            order.write(vals)
            return order
        else:
            return super(SaleOrder, self).create(vals)

    @api.model
    def pos_order_filter(self, orders_dict):
        res = []
        for order_dict in orders_dict:
            order = self.browse(order_dict['id'])
            pos_order = True
            for order_line in order.order_line:
                if not order_line.product_id.available_in_pos:
                    pos_order = False
                    break
            if pos_order:
                res.append(order_dict)

        return res

    @api.model
    def search_read_orders(self, query):
        condition = [
            ('state', '=', 'draft'),
            '|',
            ('name', 'ilike', query),
            ('partner_id', 'ilike', query)
        ]
        fields = ['name', 'partner_id', 'amount_total']
        res = self.search_read(condition, fields, limit=10)
        return self.pos_order_filter(res)

    @api.one
    def load_order(self):
        condition = [('order_id', '=', self.id)]
        fields = ['product_id', 'price_unit', 'product_uom_qty', 'discount']
        orderlines = self.order_line.search_read(condition, fields)
        return {
            'id': self.id,
            'name': self.name,
            'partner_id': self.partner_id and self.partner_id.id or False,
            'orderlines': orderlines
        }
