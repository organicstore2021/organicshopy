# -*- coding: utf-8 -*-
# from odoo import http


# class StockScarpProduct(http.Controller):
#     @http.route('/stock_scarp_product/stock_scarp_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_scarp_product/stock_scarp_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_scarp_product.listing', {
#             'root': '/stock_scarp_product/stock_scarp_product',
#             'objects': http.request.env['stock_scarp_product.stock_scarp_product'].search([]),
#         })

#     @http.route('/stock_scarp_product/stock_scarp_product/objects/<model("stock_scarp_product.stock_scarp_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_scarp_product.object', {
#             'object': obj
#         })
