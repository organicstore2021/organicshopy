# -*- coding: utf-8 -*-
# from odoo import http


# class MultPartnerPayments(http.Controller):
#     @http.route('/mult_partner_payments/mult_partner_payments/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mult_partner_payments/mult_partner_payments/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mult_partner_payments.listing', {
#             'root': '/mult_partner_payments/mult_partner_payments',
#             'objects': http.request.env['mult_partner_payments.mult_partner_payments'].search([]),
#         })

#     @http.route('/mult_partner_payments/mult_partner_payments/objects/<model("mult_partner_payments.mult_partner_payments"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mult_partner_payments.object', {
#             'object': obj
#         })
