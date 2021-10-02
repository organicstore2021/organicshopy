# -*- coding: utf-8 -*-
#partner_moves_report_id
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import  UserError


class partner_moves_reportWizard(models.TransientModel):
    _name = "partner_moves_report.wizard"
    _description = "partner_moves_report wizard"

    def compute_user_customers(self):
        user_customers = False
        config_id = self.env['sales.person.config'].search([('sale_person_id', '=', self.env.user.id)])
        if config_id and not self.env.user.has_group('sales_team.group_sale_manager'):
            if config_id.customers == 'related':
                user_customers =  self.env['res.partner'].search([('user_id', '=', self.env.user.id)]).ids
            else:
                user_customers = config_id.allowed_customers.ids
        if self.env.user.has_group('sales_team.group_sale_manager'):
            user_customers = self.env['res.partner'].search([('customer_rank', '>', 0)]).ids

        return [('id', 'in', user_customers)]
    
    partner_ids = fields.Many2one('res.partner', string='Partner', required=False, domain=compute_user_customers)
    partner_tags = fields.Many2many('res.partner.category', string='Partners Tags', required=False)
    date_from = fields.Date(string='Start Date',default=datetime.today(),required=True)
    date_to = fields.Date(string='End Date',default=datetime.today(),required=True)
    invoice_detail = fields.Boolean(string='With Invoice Detail')
    sales_man_id = fields.Many2one('hr.employee', string='Sales Man',domain=[('is_sales_man', '=', True)])
    # user_customers = fields.Many2many('res.users', string='User Customers', compute='compute_user_customers')




    def check_report(self):
        config_id = self.env['sales.person.config'].search([('sale_person_id', '=', self.env.user.id)])
        if config_id and not self.env.user.has_group('sales_team.group_sale_manager'):
            if not self.partner_ids:
                raise UserError('Please Select Customer!')
        data = {}
        data['form'] = self.read(['partner_ids', 'date_from', 'date_to','invoice_detail'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['partner_ids', 'date_from', 'date_to','invoice_detail'])[0])
        data['form'].update({'active_model1':"partner_moves_report.wizard",'active_id1':self.id})
        return self.env.ref('sales_person_reports.action_report_partner_moves_report').report_action([], data=data)
