# -*- coding: utf-8 -*-
# from odoo import http


# class PosAnalytic(http.Controller):
#     @http.route('/pos_analytic/pos_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_analytic/pos_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_analytic.listing', {
#             'root': '/pos_analytic/pos_analytic',
#             'objects': http.request.env['pos_analytic.pos_analytic'].search([]),
#         })

#     @http.route('/pos_analytic/pos_analytic/objects/<model("pos_analytic.pos_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_analytic.object', {
#             'object': obj
#         })
