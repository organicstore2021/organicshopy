# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesPersonConfig(models.Model):
    _name = 'sales.person.config'
    _rec_name = 'sale_person_id'

    sale_person_id = fields.Many2one('res.users', string='Sale Person', required=True)
    customers = fields.Selection([('related', 'Related customer'), ('all', 'All Customers')], string='Show', required=True)
    allowed_customers = fields.Many2many('res.partner', string='Allowed Customers')
    allowed_location = fields.Many2many('stock.location', string='Allowed Location', required=True)

    @api.model
    def create(self, values):
        res = super(SalesPersonConfig, self).create(values)
        allowed_location = res.allowed_location
        for location in allowed_location:
            location.write({'allowed_users': [(4, res.sale_person_id.id)]})
        return res

    def write(self, vals):
        res = super(SalesPersonConfig, self).write(vals)
        print(vals,self.sale_person_id)
        if 'allowed_location' in vals:
            allowed_location = self.env['stock.location'].browse(self.allowed_location.ids)
            for location in allowed_location:
                location.write({'allowed_users': [(4, self.sale_person_id.id)]})
            users_locations = self.env['stock.location'].search([('allowed_users', 'in', self.sale_person_id.id)])
            if len(self.allowed_location) < len(users_locations):
                user_new_locations = users_locations.search([('id', 'not in', self.allowed_location.ids)])
                for user in user_new_locations:
                    user.write({'allowed_users': [(3, self.sale_person_id.id)]})
        return res
class StockLocation(models.Model):
    _inherit = 'stock.location'


    allowed_users = fields.Many2many('res.users', string='Allowed Users')
