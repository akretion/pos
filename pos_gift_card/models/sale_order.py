# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    gift_card_id = fields.Many2one(comodel_name="gift.card")

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        res["gift_card_line_ids"] = ui_order.get("gift_card_line_ids")
        return res

