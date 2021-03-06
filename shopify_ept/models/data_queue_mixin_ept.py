from odoo import models


class DataQueueMixinEpt(models.AbstractModel):
    """ Mixin class for delete unused data queue from database."""
    _inherit = 'data.queue.mixin.ept'

    def delete_data_queue_ept(self, queue_data=[], is_delete_queue=False):
        """
        This method will delete completed data queues from database.
        @author: Keyur Kanani
        :return: True
        """
        queue_data += ['shopify_product_data_queue_ept', 'shopify_order_data_queue_ept',
                       'shopify_customer_data_queue_ept']
        return super(DataQueueMixinEpt, self).delete_data_queue_ept(queue_data, is_delete_queue)
