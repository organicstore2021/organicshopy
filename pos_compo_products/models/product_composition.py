# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api, _
from odoo.exceptions import UserError


class CompositionProduct(models.Model):
    _name = "product.composition"
    _description = "Product packs"

    @api.onchange('product_id')
    def product_id_onchange(self):
        return {'domain': {'product_id': [('is_composition', '=', False)]}}

    name = fields.Char('name')
    product_template_id = fields.Many2one('product.template', 'Item')
    product_quantity = fields.Float('Quantity', default='1', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    price = fields.Float('Product_price')

class ComboProductTemplate(models.Model):
    _inherit = "product.template"
 
    is_composition = fields.Boolean('Composition Product', default=False)
    composition_product_id = fields.One2many('product.composition', 'product_template_id', 'Composition Item')

    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company.id)

    @api.model
    def create(self, vals):
        res = super(ComboProductTemplate, self).create(vals)


        list_price = standard_price = 0.0
        if res.is_composition and res.composition_product_id:
            for line in res.composition_product_id:
                list_price = list_price + (line.product_id.list_price * line.product_quantity)
                standard_price = standard_price + (line.product_id.standard_price * line.product_quantity)


            res.list_price = list_price
            res.standard_price = standard_price


        return res

    def write(self, vals):
        res = super(ComboProductTemplate, self).write(vals)

        if 'composition_product_id' in vals:
            list_price = standard_price = 0.0
            if self.is_composition and self.composition_product_id:
                for line in self.composition_product_id:
                    list_price = list_price + (line.product_id.list_price * line.product_quantity)
                    standard_price = standard_price + (line.product_id.standard_price * line.product_quantity)


            self.list_price = list_price
            self.standard_price = standard_price


        return res
