# Copyright (C) 2022 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_gift_card = fields.Boolean(default=False)


class PoSPayment(models.Model):
    _inherit = "pos.payment"

    gift_card_with_code = fields.Boolean(default=False)
    gift_card_amount = fields.Integer()
    gift_card_selected_id = fields.Many2one("gift.card")

    def _export_for_ui(self, payment):
        result = super()._export_for_ui(payment)
        result.update({
            'gift_card_with_code': payment.gift_card_with_code,
            'gift_card_amount': payment.gift_card_amount,
            'gift_card_selected_id': payment.gift_card_selected_id.id,
        })
        return result

    def _set_gift_card_line(self, values):
        card_id = values['gift_card_selected_id']['id']
        gift_card_id = self.env["gift.card"].browse(card_id)
        amount = values["amount"]
        code = gift_card_id.code
        if not values.get('gift_card_with_code'):
            code = False
        gift_card_line = self._create_gift_card_line(amount, gift_card_id, code)
        gift_card_line.pos_payment_id = self.id
        return gift_card_line

    def _create_gift_card_line(self, amount, card, code):
        line = self.env["gift.card.line"].create(
            {
                "gift_card_id": card.id,
                "name": card.name,
                "beneficiary_id": card.beneficiary_id.id,
                "code": code,
                "amount_used": amount,
            }
        )
        return line

    def create(self, values):
        if values['payment_method_id'] == self.env.ref("pos_gift_card.pos_payment_method_gift_card").id:
            self._set_gift_card_line(values)
            values['gift_card_selected_id'] = values['gift_card_selected_id']['id']
        return super().create(values)



