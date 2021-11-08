# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from dateutil.parser import parse
from num2words import num2words
from odoo.addons.sales_person_reports.models.num_to_text_ar import amount_to_text_arabic
from operator import itemgetter
from odoo.tools import ustr


class ReportSalesperson(models.AbstractModel):
	_name = 'report.sales_person_reports.report_partner_moves_report'

	@api.model
	def _get_report_values(self, docids, data=None):
		cr = self.env.cr

		dataaas = []
		self.model = data['form']['active_model1']
		docs = self.env[self.model].browse(data['form']['active_id1'])
		move_lines = []
		invoice_lines = []
		vendor_invoice_lines=[]
		partners_tag_obj = self.env['res.partner']
		ml_obj = self.env['account.move.line']

		d_from = docs.date_from
		d_to = docs.date_to
		s_man = docs.sales_man_id
		partners_ids = []
		if docs.partner_ids:
			partners_ids = docs.partner_ids
		else:
			for pa in docs.partner_tags:
				partners_ids = partners_tag_obj.search([('category_id', '=', pa.id)])

		for i in partners_ids:
			move_lines = []
			if s_man:
				sql= (" select aml.id as iid from account_move_line aml \
					WHERE aml.partner_id = %s and aml.sales_man_id = %s or  aml.sales_man_id=null ORDER BY aml.date asc,aml.id asc \
				")
				params = (i.id,s_man.id,)
				cr.execute(sql, params)
				orders= ml_obj.browse([x['iid'] for x in cr.dictfetchall()])


			else:
				sql= (" select aml.id as iid from account_move_line aml " \
				"WHERE aml.partner_id = %s ORDER BY aml.date asc,aml.id asc")
				params = (i.id,)
				cr.execute(sql, params)
				orders= ml_obj.browse([x['iid'] for x in cr.dictfetchall()])
			total = {'debit': 0.0, 'credit': 0.0, 'balance': 0.0}
			pre_total = {'debit': 0.0, 'credit': 0.0, 'balance': 0.0}
			is_pre_total = False
			invoice_detail = False
			balance = 0
			name = ''
			if docs.date_from and docs.date_to:
				for order in orders:
					if order.date < d_from and \
							order.account_id.id == i.property_account_receivable_id.id:
						is_pre_total = True
						pre_total['debit'] += abs(
							round(order.debit, 2))
						pre_total['credit'] += abs(
							round(order.credit, 2))
						pre_total['balance'] += abs(round(order.debit, 2)) - \
							abs(round(order.credit, 2))

						total['debit'] += abs(
							round(order.debit, 2))
						total['credit'] += abs(
							round(order.credit, 2))
						total['balance'] += abs(round(order.debit, 2)) - \
							abs(round(order.credit, 2))

					# vendors
					elif order.date < d_from and \
							order.account_id.id == i.property_account_payable_id.id:
						is_pre_total = True
						pre_total['debit'] += abs(
							round(order.debit, 2))
						pre_total['credit'] += abs(
							round(order.credit, 2))
						pre_total['balance'] += abs(round(order.debit, 2)) - \
							abs(round(order.credit, 2))

						total['debit'] += abs(
							round(order.debit, 2))
						total['credit'] += abs(
							round(order.credit, 2))
						total['balance'] += abs(round(order.debit, 2)) - \
							abs(round(order.credit, 2))

					elif d_from <= order.date \
							and order.date <= d_to and order.account_id.id == i.property_account_receivable_id.id:
						total['debit'] += abs(
							round(order.debit, 2))
						total['credit'] += abs(
							round(order.credit, 2))
						total['balance'] += abs(round(order.debit, 2)) - abs(round(order.credit, 2))
						
						move_lines.append(
							{'order': order ,'n':order.move_id.name,'id':order.id,'date':order.date,'balance': total['balance']})

					# vendors
					elif d_from <= order.date \
							and order.date <= d_to and order.account_id.id == i.property_account_payable_id.id:
						total['debit'] += abs(
							round(order.debit, 2))
						total['credit'] += abs(
							round(order.credit, 2))
						total['balance'] += abs(round(order.debit, 2)) - \
							abs(round(order.credit, 2))

						move_lines.append(
							{'order': order ,'n':order.move_id.name,'id':order.id,'date':order.date,'balance': total['balance']})
						
			else:
				raise UserError("Please enter duration")
			docargs_o = {
					'doc_ids': self.ids,
					'doc_model': self.model,
					'docs': docs,
					'time': time,
					'pre_total': pre_total,
					'orders': move_lines,
					'invoices': invoice_lines,
					'total': total,
					'total_words': amount_to_text_arabic(abs(total['balance']), 'SAR'),
					'total_words_en': amount_to_text_arabic(abs(total['balance']), 'SAR'),
					'is_pre_total':is_pre_total,
					'invoice_detail':invoice_detail,
					'partner_id':i,
				}

			dataaas.append(docargs_o)
		docargs = {
					'doc_ids': self.ids,
					'doc_model': self.model,
					'docs': docs,
					'time': time,
					'dataaas':dataaas,
				}
		

		return {
					'doc_ids': self.ids,
					'doc_model': self.model,
					'docs': docs,
					'time': time,
					'dataaas':dataaas,
				}



