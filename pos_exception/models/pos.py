# Copyright 2019 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ExceptionRule(models.Model):
    _inherit = 'exception.rule'

    model = fields.Selection(
        selection_add=[
            ('pos.order', 'Pos order'),
            ('pos.order.line', 'Pos order line'),
        ])
    pos_ids = fields.Many2many(comodel_name='pos.order', string="Pos")


class PosOrder(models.Model):
    _inherit = ['pos.order', 'base.exception']
    _name = 'pos.order'
    _order = 'main_exception_id asc, date_order desc, name desc'

    @api.model
    def _reverse_field(self):
        return 'pos_ids'

    def detect_exceptions(self):
        all_exceptions = super().detect_exceptions()
        lines = self.mapped('lines')
        all_exceptions += lines.detect_exceptions()
        return all_exceptions

    @api.constrains('ignore_exception', 'lines', 'state')
    def pos_check_exception(self):
        orders = self.filtered(lambda s: s.state == 'invoiced')
        if orders:
            orders._check_exception()

    @api.onchange('lines')
    def onchange_ignore_exception(self):
        if self.state == 'invoiced':
            self.ignore_exception = False

    def _pos_get_lines(self):
        self.ensure_one()
        return self.lines

    @api.model
    def _get_popup_action(self):
        return self.env.ref('pos_exception.action_pos_exception_confirm')
