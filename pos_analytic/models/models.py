# -*- coding: utf-8 -*-
from odoo import models, api,fields


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _prepare_line(self, order_line):

        res = super(PosSession, self)._prepare_line(order_line)
        res.update({
            'analytic': True,
            'analytic_tag_ids': self.config_id.analytic_tag_ids.ids,
            'analytic_account_id': self.config_id.account_analytic_id.id,
        })

        return res
    
    def _get_tax_vals(self, key, amount, amount_converted, base_amount):

        res = super(PosSession, self)._get_tax_vals(key, amount, amount_converted, base_amount)
        res.update({
            'analytic_tag_ids': self.config_id.analytic_tag_ids.ids,
            'analytic_account_id': self.config_id.account_analytic_id.id,
        })

        return res

    
    def _get_sale_vals(self, key, amount, amount_converted):
        # print(key,'Sale')

        res = super(PosSession, self)._get_sale_vals(key, amount, amount_converted)
        res.update({
            'analytic_tag_ids': self.config_id.analytic_tag_ids.ids,
            'analytic_account_id': self.config_id.account_analytic_id.id,
        })

        return res

class PosConfig(models.Model):
    _inherit = 'pos.config'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
