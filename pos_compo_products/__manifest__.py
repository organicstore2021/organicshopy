# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "POS Custom",
    'version': '1.0',
    'summary': '',
    'description': '',
    'category': 'Custom',
    'website': '',
    'depends': ['base', 'product', 'stock_account','point_of_sale','purchase','stock_landed_costs','product_expiry','sale','sale_stock'],

    'data': [
	'security/ir.model.access.csv',
	'views/composition_product_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
