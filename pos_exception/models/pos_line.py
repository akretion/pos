# © 2019 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class PosOrderLine(models.Model):
    _inherit = ['pos.order.line', 'base.exception.method']
    _name = 'pos.order.line'

    ignore_exception = fields.Boolean(
        related='order_id.ignore_exception',
        store=True,
        string="Ignore Exceptions")

    def _get_main_records(self):
        return self.mapped('order_id')

    @api.model
    def _reverse_field(self):
        return 'pos_ids'

    def _detect_exceptions(self, rule):
        records = super()._detect_exceptions(rule)
        return records.mapped('order_id')

    @api.model
    def test_pos_orders(self):
        lines = self.search([])
        lines.detect_exceptions()
        return True

    @api.model
    def _check_matching_sub_total(self):
        if self.id < 43769:
            return False
        precision = self.env['decimal.precision'].precision_get('Account')
        theo_sub_tot = self.qty * self.price_unit * (100 - self.discount) / 100
        if float_compare(theo_sub_tot, self.price_subtotal_incl,
                         precision_digits=precision) > 0:
            import pdb; pdb.set_trace()
            return True
        return False
