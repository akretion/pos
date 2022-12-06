# Copyright 2022 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "POS No Preload Product Image",
    "summary": "Do not preload images.",
    "version": "14.0.1.0.1",
    "category": "Point of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["hparfr"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "views/templates.xml",
    ],
}
