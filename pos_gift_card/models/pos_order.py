# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class PosPayment(models.Model):
    _inherit = "pos.payment"
    gift_card_id = fields.Many2one(comodel_name="gift.card")



class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        fields = super()._payment_fields(order, ui_paymentline)

        fields.update({
            'gift_card_with_code': ui_paymentline.get('gift_card_with_code'),
            'gift_card_amount': ui_paymentline.get('gift_card_amount'),
            'gift_card_selected_id': ui_paymentline.get('gift_card_selected_id'),
        })
        return fields

    # def add_payment(self, data):
    #     self.ensure_one()
    #     if data.get('gift_card_selected_id'):
    #         print(f"// data.get('gift_card_selected_id') : {data.get('gift_card_selected_id')}")
    #         data["gift_card_selected_id"] = data['gift_card_selected_id'].get('id')
    #     return super().add_payment(data)
