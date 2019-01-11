# -*- coding: utf-8 -*-
# Copyright (C) 2017 (https://akretion.com)
# @author: Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# @author: Raphael Reverdy (https://akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'PoS Pay Sale Order',
    'version': '10.0.1.0.0',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'depends': [
        'pos_order_to_sale_order',
    ],
    'website': 'https://odoo-community.org/',
    'data': [
        'views/sale_order_view.xml',
        'views/pos_pay_sale_order.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/pos_pay_sale_order.xml',
    ],
}
