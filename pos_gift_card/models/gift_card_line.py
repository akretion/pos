# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class GiftCardLine(models.Model):
    _inherit = "gift.card.line"

    pos_order_id = fields.Many2one(comodel_name="pos.order")

    pos_payment_id = fields.Many2one(
        comodel_name="pos.payment",
        string="Pos Payment",
        compute="_compute_pos_payment_id",
        store=True,
        )

    @api.depends("pos_order_id.payment_ids")
    def _compute_pos_payment_id(self):
        for rec in self:
            rec.pos_payment_id = self.env["pos.payment"].search([("gift_card_selected_id","=", rec.gift_card_id.id), ("pos_order_id","=",rec.pos_order_id.id)], limit=1)

