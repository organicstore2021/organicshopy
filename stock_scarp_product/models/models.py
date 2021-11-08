# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    exp_date = fields.Date(string='EXP Date', compute='compute_exp_date', store=True)

    @api.depends('removal_date')
    def compute_exp_date(self):
        for rec in self:
            rec.exp_date = False
            if rec.removal_date:
                rec.exp_date = rec.removal_date.date()

    @api.model
    def create_scrap(self):
        scrap_location_id = self.env['stock.location'].browse(
            int(self.env['ir.config_parameter'].sudo().get_param('stock_scarp_product.scrap_location_id')))
        lot_ids = self.env['stock.production.lot'].search([('removal_date', '<=', fields.Datetime.now())])
                                                           # ('exp_date', '=', fields.Date.today())])
        for rec in lot_ids:
            if rec.product_qty > 0.0:
                print('LOT', rec.product_qty)
                quant_ids = self.env['stock.quant'].search([('location_id.usage', '=', 'internal'),('lot_id', '=', rec.id), ('quantity', '>', 0.0),('product_id', '=', rec.product_id.id)])
                for quant in quant_ids:
                    if quant.quantity > 0.0:
                        scrapped = self.env['stock.scrap'].create({
                            'product_id': rec.product_id.id,
                            'lot_id': rec.id,
                            'scrap_qty':quant.quantity,
                            'product_uom_id':quant.product_uom_id.id,
                            'location_id':quant.location_id.id,
                            'scrap_location_id':scrap_location_id.id,
                        })
                        scrapped.action_validate()




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    scrap_location_id = fields.Many2one('stock.location', string='Operation Type',
                                          domain=[('usage', '=', 'inventory')])

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['scrap_location_id'] = int(get_param('stock_scarp_product.scrap_location_id'))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('stock_scarp_product.scrap_location_id', int(self.scrap_location_id.id))

