# Copyright (C) 2022 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class GiftCard(models.Model):
    _inherit = "gift.card"

    pos_order_ids = fields.Many2many(
        comodel_name="sale.order",
        compute="_compute_pos_order_ids",
        string="POS Orders",
        readonly=True,
        )

    @api.depends("gift_card_line_ids.pos_order_id")
    def _compute_pos_order_ids(self):
        for rec in self:
            rec.pos_order_ids = rec.gift_card_line_ids.mapped("pos_order_id").ids


