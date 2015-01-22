# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Akretion (<http://www.akretion.com>).
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

    def _order_fields(self, cr, uid, ui_order, context=None):
        context = context or {}
        res = super(PosOrder, self)._order_fields(cr, uid, ui_order, context)
        if 'order_id' in ui_order:
            res['order_id'] = ui_order['order_id']
        return res

    @api.model
    def search_read_orders(self, query):
        condition = ['|',
            ('pos_reference', 'ilike', query),
            ('partner_id', 'ilike', query)
        ]
        fields = ['pos_reference', 'partner_id']
        return self.search_read(condition, fields, limit=10)

    @api.one
    def load_order(self):
        condition = [('order_id', '=', self.id)]
        fields = ['product_id', 'price_unit', 'qty', 'discount']
        orderlines = self.lines.search_read(condition, fields)
        return {
            'id': self.id,
            'name': self.pos_reference,
            'partner_id': self.partner_id and self.partner_id.id or False,
            'orderlines': orderlines
        }
