# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class GiftCardLine(models.Model):
    _inherit = "gift.card.line"

    pos_payment_id = fields.Many2one(
        comodel_name="pos.payment",
        readonly=True)

    pos_order_ids = fields.Many2many(
        comodel_name="pos.order",
        compute="_compute_pos_order_ids",
        readonly=True
    )

    @api.depends("pos_payment_id")
    def _compute_pos_order_ids(self):
        for rec in self:
            rec.pos_order_ids = rec.pos_payment_id.mapped("pos_order_id")