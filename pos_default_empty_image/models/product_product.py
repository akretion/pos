# Copyright (C) 2017 - Today:
#   GRAP (http://www.grap.coop)
#   Akretion (http://www.akretion.com)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends("image_variant_1920", "product_tmpl_id.image_1920")
    def _compute_has_image(self):
        for product in self:
            product.has_image = product.image_variant_1920 or product.product_tmpl_id.image_1920

    has_image = fields.Boolean(
        compute="_compute_has_image", string="Has Image", store=True
    )
