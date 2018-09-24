# -*- coding: utf-8 -*-
# @author: Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    anonymous_partner_id = fields.Many2one(
        'res.partner',
        string='Anonymous Partner')
