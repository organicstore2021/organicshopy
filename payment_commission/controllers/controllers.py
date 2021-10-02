# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentComission(http.Controller):
#     @http.route('/payment_comission/payment_comission/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_comission/payment_comission/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_comission.listing', {
#             'root': '/payment_comission/payment_comission',
#             'objects': http.request.env['payment_comission.payment_comission'].search([]),
#         })

#     @http.route('/payment_comission/payment_comission/objects/<model("payment_comission.payment_comission"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_comission.object', {
#             'object': obj
#         })
