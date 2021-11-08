# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    collect_payment = fields.Boolean(string='Collect Payments')
    commission_ids = fields.One2many('commission.config', 'user_id', string='Commission Config')

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields):
        result = super(AccountPayment, self).default_get(fields)
        if self.env.user.partner_id.collect_payment:
            result['sale_person_id'] = self.env.user.partner_id.id
        return result

    sale_person_id = fields.Many2one('res.partner', string='Sale Person', required=True)
    commission_amount = fields.Float(string='Commission', compute='compute_commission_amount', strore=True)

    @api.depends('sale_person_id.collect_payment', 'amount', 'payment_type', 'payment_date')
    def compute_commission_amount(self):
        for rec in self:
            rec.commission_amount = 0.0
            payment_day = 0
            if rec.payment_date:
                print("....... ", rec)
                print("....... ", rec.payment_date)
                payment_day = 27 #rec.payment_date.day()
            commission_days =  0.0
            commission_id = False
            if rec.sale_person_id and rec.amount > 0.0 and rec.payment_type == 'inbound' and rec.sale_person_id.collect_payment:
                commission_ids = rec.sale_person_id.commission_ids
                for commission in commission_ids:
                    if commission_days < payment_day <= commission.month_days:
                        commission_id = commission
                    else:
                        commission_days = commission.month_days
                type = commission_id.type
                if type == 'percentage':
                    rec.commission_amount = rec.amount * commission_id.percentage_commission / 100
                elif type == 'fix':
                    rec.commission_amount = commission_id.amount_commission
                else:
                    rec.commission_amount = rec.amount * commission_id.percentage_commission / 100 + commission_id.amount_commission


class CommissionConfig(models.Model):
    _name = 'commission.config'

    user_id = fields.Many2one('res.partner', string='Sale Person')
    month_days = fields.Integer(string='To Day Of Month', required=True)
    type = fields.Selection([('percentage', 'Percentage'), ('fix', 'Fixed Amount'), ('percentage_fix', 'Percentage + Fix Amount')], string='Commission Type', required=True)
    percentage_commission = fields.Float(string='Percentage%', required=True)
    amount_commission = fields.Float(string='Amount')


