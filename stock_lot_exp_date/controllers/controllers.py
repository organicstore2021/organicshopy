# -*- coding: utf-8 -*-
# from odoo import http


# class StockLotExpDate(http.Controller):
#     @http.route('/stock_lot_exp_date/stock_lot_exp_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_lot_exp_date/stock_lot_exp_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_lot_exp_date.listing', {
#             'root': '/stock_lot_exp_date/stock_lot_exp_date',
#             'objects': http.request.env['stock_lot_exp_date.stock_lot_exp_date'].search([]),
#         })

#     @http.route('/stock_lot_exp_date/stock_lot_exp_date/objects/<model("stock_lot_exp_date.stock_lot_exp_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_lot_exp_date.object', {
#             'object': obj
#         })
