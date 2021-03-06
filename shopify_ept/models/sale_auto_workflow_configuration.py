from odoo import models, fields

class SaleAutoWorkflowConfiguration(models.Model):
    _name = "sale.auto.workflow.configuration.ept"
    _description = 'Sale auto workflow configuration'

    def _default_payment_term(self):
        payment_term = self.env.ref("account.account_payment_term_immediate")
        return payment_term.id if payment_term else False
    financial_status = fields.Selection([('pending', 'The finances are pending'),
                                         ('authorized', 'The finances have been authorized'),
                                         (
                                         'partially_paid', 'The finances have been partially paid'),
                                         ('paid', 'The finances have been paid'),
                                         ('partially_refunded',
                                          'The finances have been partially refunded'),
                                         ('refunded', 'The finances have been refunded'),
                                         ('voided', 'The finances have been voided')
                                         ], default="paid", required=1)
    auto_workflow_id = fields.Many2one("sale.workflow.process.ept", "Auto Workflow", required=1)
    payment_gateway_id = fields.Many2one("shopify.payment.gateway.ept", "Payment Gateway",
                                         required=1)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Term', default=_default_payment_term)
    shopify_instance_id = fields.Many2one("shopify.instance.ept", "Instance", required=1)
    active = fields.Boolean(default=True)
    _sql_constraints = [('_workflow_unique_constraint',
                         'unique(financial_status,shopify_instance_id,payment_gateway_id)',
                         "Financial status must be unique in the list")]

    def create_financial_status(self, instance, financial_status):
        """
        Creates financial status for payment methods of instance.
        @param instance:
        @param financial_status: Status as paid or not paid.
        """
        payment_methods = self.env['shopify.payment.gateway.ept'].search([('shopify_instance_id', '=', instance.id)])
        auto_workflow_record = self.env.ref("auto_invoice_workflow_ept.automatic_validation_ept")

        for payment_method in payment_methods:
            domain = [('shopify_instance_id', '=', instance.id),
                      ('payment_gateway_id', '=', payment_method.id),
                      ('financial_status', '=', financial_status)]

            existing_financial_status = self.search(domain).ids
            if existing_financial_status:
                continue

            vals = {
                'shopify_instance_id': instance.id,
                'auto_workflow_id': auto_workflow_record.id,
                'payment_gateway_id': payment_method.id,
                'financial_status': financial_status
            }
            self.create(vals)
        return True

