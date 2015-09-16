# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Today Akretion (<http://www.akretion.com>).
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

from openerp import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    partner_ref = fields.Char(string='Client Ref', related='partner_id.ref')
    partner_name = fields.Char(string='Client Name', related='partner_id.name')
    xml_sale_receipt = fields.Text(string='XML Sale receipt')

    @api.model
    def search_read_orders_reprint(self, query):
        domain = []
        if (query):
            domain += [
                '|',
                '|',
                ('partner_ref', 'ilike', query),
                ('partner_id', 'ilike', query),
                ('name', 'ilike', query),
            ]
        fields = [
            'id', 'date_order', 'name', 'partner_name',
            'partner_ref', 'amount_total',
        ]
        return self.search_read(domain, fields, limit=10)

    @api.one
    def load_xml_sale_receipt(self):
        return {
            'xml_sale_receipt': self.xml_sale_receipt,
        }
        return res

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['xml_sale_receipt'] = ui_order['xml_sale_receipt']
        return res
