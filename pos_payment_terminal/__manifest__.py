# -*- coding: utf-8 -*-
{
    'name': 'POS Payment Terminal (Ingenico Caisse-AP)',
    'version': '18.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Connect Ingenico Terminals via Direct Sockets',
    'description': """
        Integrates Ingenico Payment Terminals (Caisse-AP Protocol)
        using Chrome Direct Sockets API and OCA IoT device management.

        Requires launching Chrome with:
        --enable-features=DirectSockets --restricted-api-origins="http://localhost:8069"
    """,
    'depends': ['point_of_sale', 'iot_oca'],
    'data': [
        'security/ir.model.access.csv',
        'views/iot_device_views.xml',
        'views/pos_payment_method_views.xml',
    ],
    'assets': {
        'point_of_sale.assets_prod': [
            'pos_payment_terminal/static/src/app/payment_caisse_ap.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
}
