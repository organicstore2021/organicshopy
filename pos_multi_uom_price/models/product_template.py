# -*- coding: utf-8 -*-


from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    multi_uom_price_id = fields.One2many('product.multi.uom.price', 'product_tem_id', _("UOM price"))



    @api.model
    def get_data(self, kw):
        multi_uom = self.env['product.multi.uom.price'].search([])
        product_ids = list(dict.fromkeys(multi_uom.product_tem_id))
        data = {}
        for product_tem_id in product_ids:
            uoms = multi_uom.filtered(lambda x: x.product_tem_id.id == product_tem_id.id)
            price_data = []
            for uom in uoms:
                price_data.append({
                    'id':uom.uom_id.id,
                    'product_id':product_tem_id.id,
                    'price':uom.price,
                    'barcode':uom.uom_barcode,
                })
            data.update({
                product_tem_id.id : price_data
            })
        return data
