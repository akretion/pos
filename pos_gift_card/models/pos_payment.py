# Copyright (C) 2022 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_gift_card = fields.Boolean(default=False)


class PoSPayment(models.Model):
    _inherit = "pos.payment"

    gift_card_id = fields.Many2one(comodel_name="gift.card")

    def _export_for_ui(self, payment):
        result = super()._export_for_ui(payment)
        result.update({
            "gift_card_id": payment.gift_card_id.id, 
        })
        return result

    def _set_gift_card_line(self, values):
        card_id = values['gift_card_id']
        gift_card_id = self.env["gift.card"].browse(card_id)
        if (not gift_card_id):
            # TODO: Raise ?
            return
        amount = values["amount"]
        gift_card_line = self._create_gift_card_line(amount, gift_card_id)
        gift_card_line.pos_payment_id = self.id
        return gift_card_line

    def _create_gift_card_line(self, amount, card):
        line = self.env["gift.card.line"].create(
            {
                "gift_card_id": card.id,
                "name": card.name,
                "beneficiary_id": self.partner_id.id,
                "amount_used": amount,
            }
        )
        return line

    def create(self, values):
        res = super().create(values)
        if res.payment_method_id.is_gift_card:
            res._set_gift_card_line(values)


