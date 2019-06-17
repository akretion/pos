# Copyright 2019 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "POS Exception",
    "summary": "Custom exceptions on Pos order",
    "version": "12.0.0.0.1",
    "category": "Point Of Sale",
    "author": "Akretion, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos.workflow",
    "depends": ["point_of_sale", "base_exception"],
    "license": "AGPL-3",
    "data": [
        "data/pos_exception_data.xml",
        "views/pos_view.xml",
    ],
}
