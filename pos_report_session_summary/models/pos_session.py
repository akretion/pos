from odoo import fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    cash_register_total_entry_encoding = fields.Monetary(
        compute="_compute_cash_total_entry_encoding",
        string="Total Cash Transaction",
        readonly=True,
    )

    def _compute_cash_total_entry_encoding(self):
        for session in self:
            session.cash_register_total_entry_encoding = (
                session.cash_register_balance_end - session.cash_register_balance_start
            )
