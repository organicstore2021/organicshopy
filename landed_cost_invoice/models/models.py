# -*- coding: utf-8 -*-

from odoo import models, fields, api

SPLIT_METHOD = [
    ('equal', 'Equal'),
    ('by_quantity', 'By Quantity'),
    ('by_current_cost_price', 'By Current Cost'),
    ('by_weight', 'By Weight'),
    ('by_volume', 'By Volume'),
]

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_landed_cost = fields.Boolean(string='Is Landed Cost Invoice')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    split_method = fields.Selection(SPLIT_METHOD, string='Split Method')

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    landed_invoice_ids = fields.Many2many('account.move', string='Landed Costs Invoices', domain=[('is_landed_cost', '=', True), ('state', '=','posted')])

    @api.onchange('landed_invoice_ids')
    def onchange_landed_invoices(self):
        cost_ids = []
        self.cost_lines = False
        #IF their are lines
        # cost_lines = self.cost_lines
        # for cost in cost_lines.filtered(lambda m: m.product_id.id not in  self.landed_invoice_ids.mapped('invoice_line_ids').mapped('product_id').ids):
        #     product_ids = {
        #         'name': cost.name,
        #         'product_id': cost.product_id.id,
        #         'price_unit': cost.price_unit,
        #         'split_method': cost.split_method or 'equal',
        #         'account_id': cost.account_id.id,
        #     }
        #     cost_ids += [(0, 0, product_ids)]
        # print(cost_ids)
        self.cost_lines = False
        for rec in self.landed_invoice_ids:
            for line in rec.invoice_line_ids.filtered(lambda m: m.is_landed_costs_line == True):
                product_ids = {
                    'name':line.name,
                    'product_id':line.product_id.id,
                    'price_unit':line.price_subtotal,
                    'split_method':line.product_id.split_method or 'equal',
                    'account_id':line.account_id.id,
                }
                if cost_ids:
                    cost_ids  += [(0, 0, product_ids)]
                else:
                    cost_ids = [(0, 0, product_ids)]
        self.cost_lines = cost_ids
