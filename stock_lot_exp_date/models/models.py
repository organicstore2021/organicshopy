# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_round, float_compare, float_is_zero



class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    exp_date = fields.Datetime(string='Expiry Date')

    @api.onchange('lot_id')
    def onchange_lot(self):
        for rec in self:
            if rec.lot_id:
                rec.exp_date = rec.lot_id.exp_date

    def _action_done(self):
        for ml in self:
            if ml.lot_name and not ml.lot_id:
                lot = self.env['stock.production.lot'].create(
                    {'name': ml.lot_name, 'product_id': ml.product_id.id, 'company_id': ml.move_id.company_id.id, 'removal_date':ml.exp_date}
                )
                ml.write({'lot_id': lot.id})
        return super(StockMoveLine, self)._action_done()