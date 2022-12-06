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
        card_id = values['gift_card_selected_id']
        gift_card_id = self.env["gift.card"].browse(card_id)
        amount = values["amount"]
        gift_card_line = self._create_gift_card_line(amount, gift_card_id)
        gift_card_line.pos_payment_id = self.id
        return gift_card_line

    def _create_gift_card_line(self, amount, card):
        line = self.env["gift.card.line"].create(
            {
                "gift_card_id": card.id,
                "name": card.name,
                "beneficiary_id": self.partner_id,
                "amount_used": amount,
            }
        )
        return line

    def create(self, values):
        payment_method = self.browse(values['payment_method_id'])
        if not payment_method:
            # TODO warning ?
            break
        else if payment_method.is_gift_card:
            self._set_gift_card_line(values)
        return super().create(values)


