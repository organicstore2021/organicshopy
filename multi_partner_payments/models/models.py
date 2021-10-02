# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class MultiPayment(models.Model):
    _name = 'multi.payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Partners Multi Payments'


    name = fields.Char(string='Name')
    ref = fields.Char(string='Reference')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    date = fields.Date(string='Date', default=fields.Date.today(), required=True)
    accounting_date = fields.Date(string='Accounting Date', default=fields.Date.today(), required=True)
    type = fields.Selection([('cash_in', 'Money In'), ('cash_out', 'Money Out')], string='Type', default='cash_in')
    payments_ids = fields.One2many('multi.payment.line', 'payment_id', string='Payments')
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted'),('cancelled', 'Cancelled')
                             ],track_visibility='onchange', default='draft')
    move_id = fields.Many2one('account.move', string='Accounting Entry')

    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 store=True, readonly=True,
                                 compute='_compute_company_id')
    currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True,
        states={'draft': [('readonly', False)]},
        string='Currency',
        copy=True,
        compute='_compute_currency_id')


    @api.depends('journal_id')
    def _compute_company_id(self):
        for mp in self:
            mp.company_id = mp.journal_id.company_id or mp.company_id or self.env.company

    
    @api.depends('journal_id')
    def _compute_currency_id(self):
        for mp in self:
            mp.currency_id = mp.journal_id.currency_id or self.env.company.currency_id


    @api.model
    def create(self, values):
        if values['type'] == 'cash_in':
            values['name'] = self.env['ir.sequence'].get('multi.payment.customer') or ' '
        if values['type'] == 'cash_out':
            values['name'] = self.env['ir.sequence'].get('multi.payment.vendor') or ' '
        res = super(MultiPayment, self).create(values)
        return res

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        for rec in self:
            if rec.state == 'posted':
                if rec.move_id:
                    rec.move_id.button_draft()

                    rec.move_id.line_ids.unlink()
            rec.state = 'draft'

    def post_multi_partner(self):
        if not self.payments_ids:
            raise UserError('Please Enter Payments')
        result = self.env['multi.payment.line'].read_group([('id', 'in', self.payments_ids.ids)], fields=['amount', 'currency_id', 'partner_id' ,'name'], groupby=['currency_id'])
        lines = []
        name = self.name

        if self.ref:
            name = name + ' - ' + self.ref


        if self.type == 'cash_in':

            for rec in self.payments_ids:
                if rec.currency_id.id != self.env.company.currency_id.id:
                    amount = -rec.amount
                    print(-rec.amount)
                    credit_line = (0,0,{
                        'account_id': rec.partner_id.property_account_receivable_id.id,
                        'partner_id':rec.partner_id.id,
                        'name':rec.name,
                        'currency_id':rec.currency_id.id,
                        'amount_currency': amount,
                        'credit': rec.amount / rec.currency_id.rate,
                        'analytic_account_id': rec.analytic_account.id
                    })
                    lines.append(credit_line)


                    rate = self.env['res.currency'].search([('id', '=', item['currency_id'][0])]).with_context(date=self.accounting_date).rate
                    debit_line = (0,0,{
                        'account_id': self.journal_id.default_debit_account_id.id,
                        'name': name,
                        'currency_id': rec.currency_id.id,
                        'amount_currency': amount,
                        'debit': rec.amount / rec.currency_id.rate,
                        'analytic_account_id': rec.analytic_account.id
                    })
                    lines.append(debit_line)

            # *********************************************************************************************************************
                else:
                    credit_line = (0,0,{
                        'account_id':rec.partner_id.property_account_receivable_id.id,
                        'partner_id': rec.partner_id.id,
                        'name': rec.name,
                        'credit': rec.amount,
                        'analytic_account_id':rec.analytic_account.id
                    })
                    lines.append(credit_line)

                    debit_line = (0,0,{
                        'account_id': self.journal_id.default_debit_account_id.id,
                        'name': name,
                        'debit': rec.amount,
                    })
                    lines.append(debit_line)


            
            # for item in result:
            #     currency_amount = item['amount']
            #     if item['currency_id'][0] != self.env.company.currency_id.id:
            #         rate = self.env['res.currency'].search([('id', '=', item['currency_id'][0])]).with_context(date=self.accounting_date).rate
            #         debit_line = (0,0,{
            #             'account_id': self.journal_id.default_debit_account_id.id,
            #             'name': self.name,
            #             'currency_id': item['currency_id'][0],
            #             'amount_currency': currency_amount,
            #             'debit': currency_amount / rate,
            #         })
            #         lines.append(debit_line)
            #     else:
            #         debit_line = (0,0,{
            #             'account_id': self.journal_id.default_debit_account_id.id,
            #             'name': name,
            #             'debit': currency_amount,
            #         })
            #         lines.append(debit_line)

        if self.type == 'cash_out':

            for rec in self.payments_ids:
                if rec.currency_id.id != self.env.company.currency_id.id:
                    debit_line = (0, 0, {
                        'account_id': rec.partner_id.property_account_payable_id.id,
                        'partner_id': rec.partner_id.id,
                        'name': rec.name,
                        'currency_id': rec.currency_id.id,
                        'amount_currency': rec.amount,
                        'debit': rec.amount / rec.currency_id.rate,
                        'analytic_account_id': rec.analytic_account.id
                    })
                    lines.append(debit_line)


                    rate = self.env['res.currency'].search([('id', '=', item['currency_id'][0])]).with_context(date=self.accounting_date).rate
                    credit_line = (0, 0, {
                        'account_id': self.journal_id.default_debit_account_id.id,
                        'name': name,
                        'currency_id': rec.currency_id.id,
                        'amount_currency': -rec.amount,
                        'credit': rec.amount / rec.currency_id.rate,
                    })
                    lines.append(credit_line)

                else:
                    debit_line = (0, 0, {
                        'account_id': rec.partner_id.property_account_payable_id.id,
                        'partner_id': rec.partner_id.id,
                        'name': rec.name,
                        'debit': rec.amount,
                        'analytic_account_id': rec.analytic_account.id
                    })
                    lines.append(debit_line)

                    credit_line = (0, 0, {
                        'account_id': self.journal_id.default_debit_account_id.id,
                        'name': name,
                        'credit': rec.amount,
                    })
                    lines.append(credit_line)
            
            # for item in result:
            #     currency_amount = item['amount']
            #     if item['currency_id'][0] != self.env.company.currency_id.id:
            #         rate = self.env['res.currency'].search([('id', '=', item['currency_id'][0])]).with_context(date=self.accounting_date).rate
            #         credit_line = (0, 0, {
            #             'account_id': self.journal_id.default_debit_account_id.id,
            #             'name': name,
            #             'currency_id': item['currency_id'][0],
            #             'amount_currency': -currency_amount,
            #             'credit': currency_amount / rate,
            #         })
            #         lines.append(credit_line)
            #     else:
            #         credit_line = (0, 0, {
            #             'account_id': self.journal_id.default_debit_account_id.id,
            #             'name': name,
            #             'credit': currency_amount,
            #         })
            #         lines.append(credit_line)


        move_id = self.env['account.move'].create({
            'type': 'entry',
            'journal_id':self.journal_id.id,
            'date':self.accounting_date,
            'ref':name,
            'line_ids':lines,
        })
        move_id.post()
        self.move_id = move_id.id
        self.state = 'posted'



class MultiPaymentLine(models.Model):
    _name = 'multi.payment.line'


    
    name  = fields.Char(string='Label', required=True)
    payment_id = fields.Many2one('multi.payment', string='Payment')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, related='payment_id.currency_id')
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    
