# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class GiftCardLine(models.Model):
    _inherit = "gift.card.line"

    pos_order_id = fields.Many2one(comodel_name="pos.order")
