# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    use_gift_card_as_payment = fields.Boolean(string="Gift Card Payment Mode")


    def setup_defaults(self, company):
        self = self._add_gift_card_payment_method(company)
        return super().setup_defaults()

    def _add_gift_card_payment_method(self, company):
        for pos_config in self:
            if pos_config.has_active_session:
                continue
            gift_card_journal = self.env.ref("gift_card.gift_card_journal")
