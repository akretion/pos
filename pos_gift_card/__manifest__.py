# Copyright 2021 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "pos_gift_card",
    "summary": "pos_gift_card",
    "version": "14.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "point_of_sale",
        "account_payment_gift_card",
        "gift_card",
    ],
    "data": [
        "views/pos_config_view.xml",
        "views/pos_assets.xml",
        "views/gift_card.xml",
        "views/gift_card_line.xml",
        "views/pos_order.xml",
        "data/data.xml",
    ],
    "demo": [],
    "qweb": [
        "static/src/xml/GiftCardPaymentLine.xml",
    ],
}
