# -*- coding: utf-8 -*-
# from odoo import http


# class LandedCostInvoice(http.Controller):
#     @http.route('/landed_cost_invoice/landed_cost_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/landed_cost_invoice/landed_cost_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('landed_cost_invoice.listing', {
#             'root': '/landed_cost_invoice/landed_cost_invoice',
#             'objects': http.request.env['landed_cost_invoice.landed_cost_invoice'].search([]),
#         })

#     @http.route('/landed_cost_invoice/landed_cost_invoice/objects/<model("landed_cost_invoice.landed_cost_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('landed_cost_invoice.object', {
#             'object': obj
#         })
