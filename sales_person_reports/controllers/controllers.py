# -*- coding: utf-8 -*-
# from odoo import http


# class SalesPersonReports(http.Controller):
#     @http.route('/sales_person_reports/sales_person_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_person_reports/sales_person_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_person_reports.listing', {
#             'root': '/sales_person_reports/sales_person_reports',
#             'objects': http.request.env['sales_person_reports.sales_person_reports'].search([]),
#         })

#     @http.route('/sales_person_reports/sales_person_reports/objects/<model("sales_person_reports.sales_person_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_person_reports.object', {
#             'object': obj
#         })
