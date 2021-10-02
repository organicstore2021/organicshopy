# -*- coding: utf-8 -*-
{
    'name': "stock_scrap_product",

    'summary': """
        Auto Remove Products Expiry""",

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'stock', 'product_expiry'],
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
