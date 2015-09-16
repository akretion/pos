# -*- coding: utf-8 -*-
# © 2015 Sylvain Calador <sylvain.calador@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "POS order reprint",
    "summary": "Allow to print receipt of past orders",
    "version": "1.0",
    "category": "Point Of Sale",
    "website": "https://odoo-community.org/",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "views/pos_order_reprint.xml",
    ],
    "qweb": [
        "static/src/xml/pos_order_reprint.xml",
    ],
    "demo": [
    ],
}
