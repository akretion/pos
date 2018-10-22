# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Raphael Reverdy (https://akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'PoS Order To Sale Order',
    'version': '10.0.1.0.0',
    'author': 'GRAP,Akretion,Odoo Community Association (OCA)',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'sale',
        'onchange_helper',
    ],
    'website': 'https://odoo-community.org/',
    'data': [
        'views/view_pos_config.xml',
        'views/pos_order_to_sale_order.xml',
        'views/pos_to_so_report.xml',
        'data/res_partner_data.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        # 'demo/product_template.xml',
        # 'demo/sale_order.xml',
        # 'demo/stock_picking_type.xml',
    ],
    'qweb': [
        'static/src/xml/pos_order_to_sale_order.xml',
    ],
}
