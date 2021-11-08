# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Company Logo In POS Receipt',
    'version': '10.0.1.2',
    'author': 'IES Team',
    'category': 'Point Of Sale',
    'depends': ['base', 'point_of_sale'],
    'license': 'LGPL-3',
    'data': [
        'views/import.xml',
        # 'views/pos_order.xml',
    ],
    'qweb': [
            'static/src/xml/pos_ticket_view.xml',
            #'static/src/libs/js/jquery-barcode-last.min.js',
            #'static/src/xml/pos.xml'
            ],
    'images': ['static/description/banner.jpg'],
    'demo': [],
    'installable': True,
    'application': True,
}
