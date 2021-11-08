# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError
from lxml import etree
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from odoo.osv.orm import setup_modifiers
from collections import namedtuple





class PosOrder(models.Model):
    _inherit = "pos.order"
 	
    def create_picking(self):
        
        self = self.with_context(pos_config=self.session_id.config_id.id)

        print(self.session_id.config_id)
        res = super(PosOrder, self).create_picking()

        return res
