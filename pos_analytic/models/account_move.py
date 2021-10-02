# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, float_is_zero

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        # This method returns a dictionary to provide an easy extension hook to modify the valuation lines (see purchase for an example)
        res = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)
            
        if 'pos_config' in self._context:
            pos_config = self.env['pos.config'].browse(self._context.get('pos_config'))
            res['debit_line_vals'].update({'analytic_account_id': pos_config.account_analytic_id.id})
            res['debit_line_vals'].update({'analytic_tag_ids': pos_config.analytic_tag_ids.ids})

            res['credit_line_vals'].update({'analytic_account_id': pos_config.account_analytic_id.id})
            res['credit_line_vals'].update({'analytic_tag_ids': pos_config.analytic_tag_ids.ids})

        return res

