# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError
from lxml import etree
import time
from odoo.tools import float_is_zero
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from odoo.osv.orm import setup_modifiers
from collections import namedtuple





class PosOrder(models.Model):
    _inherit = "pos.order"
 	
    def create_picking(self):
        """Create a picking for each order and validate it."""
        Picking = self.env['stock.picking']
        Move = self.env['stock.move']
        StockWarehouse = self.env['stock.warehouse']
        for order in self:
            if not order.lines.filtered(lambda l: l.product_id.type in ['product', 'consu']):
                continue
            address = order.partner_id.address_get(['delivery']) or {}
            picking_type = order.picking_type_id
            return_pick_type = order.picking_type_id.return_picking_type_id or order.picking_type_id
            order_picking = Picking
            return_picking = Picking
            moves = Move
            location_id = order.location_id.id
            if not location_id:
                location_id = order.picking_type_id.default_location_src_id.id
            if order.partner_id:
                destination_id = order.partner_id.property_stock_customer.id
            else:
                if (not picking_type) or (not picking_type.default_location_dest_id):
                    customerloc, supplierloc = StockWarehouse._get_partner_locations()
                    destination_id = customerloc.id
                else:
                    destination_id = picking_type.default_location_dest_id.id

            if picking_type:
                
                message = _("This transfer has been created from the point of sale session: <a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
                picking_vals = {
                    'origin': order.name,
                    'partner_id': address.get('delivery', False),
                    'date_done': order.date_order,
                    'picking_type_id': picking_type.id,
                    'company_id': order.company_id.id,
                    'move_type': 'direct',
                    'note': order.note or "",
                    'location_id': location_id,
                    'location_dest_id': destination_id,
                }
                pos_qty = any([x.qty > 0 for x in order.lines if x.product_id.type in ['product', 'consu']])
                if pos_qty:
                    order_picking = Picking.create(picking_vals.copy())
                    order_picking.message_post(body=message)
                neg_qty = any([x.qty < 0 for x in order.lines if x.product_id.type in ['product', 'consu']])
                if neg_qty:
                    return_vals = picking_vals.copy()
                    return_vals.update({
                        'location_id': destination_id,
                        'location_dest_id': return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                        'picking_type_id': return_pick_type.id
                    })
                    return_picking = Picking.create(return_vals)
                    return_picking.message_post(body=message)

            for line in order.lines.filtered(lambda l: l.product_id.type in ['product', 'consu'] or l.product_id.is_composition == True):
                if line.product_id.is_composition:
                    qty = line.qty
                    if qty <= 0:
                        qty = abs(line.qty * -1)
                    else:
                        qty = abs(line.qty)
                    
                    

                    for dd in line.product_id.composition_product_id:

                        # if dd.product_id.is_composition:

                        #     for ddd in dd.product_id.composition_product_id:
                        #         moves |= Move.create(self.create_composition_product(line, ddd, order_picking, return_picking, qty, picking_type, return_pick_type, location_id, destination_id))
                                
                        # else:
                        moves |= Move.create({
                            'name': line.name,
                            'product_uom': dd.uom_id.id, ##dd.uom_id.id,
                            'picking_id': order_picking.id if dd.product_quantity * line.qty >= 0 else return_picking.id,
                            'picking_type_id': picking_type.id if dd.product_quantity * line.qty >= 0 else return_pick_type.id,
                            'product_id': dd.product_id.id,
                            'product_uom_qty': abs(dd.product_quantity) * qty * (line.uom_id.factor_inv if line.uom_id.uom_type == 'bigger' else line.uom_id.factor) ,
                            'state': 'draft',
                            'location_id': location_id if dd.product_quantity * qty >= 0 else destination_id,
                            'location_dest_id': destination_id if dd.product_quantity * qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                        })
                        
                        # if line.product_id.type == 'product':
                        #     moves |= Move.create({
                        #         'name': line.name,
                        #         'product_uom': line.uom_id.id, #line.product_id.uom_id.id,
                        #         'picking_id': order_picking.id if line.qty >= 0 else return_picking.id,
                        #         'picking_type_id': picking_type.id if line.qty >= 0 else return_pick_type.id,
                        #         'product_id': line.product_id.id,
                        #         'product_uom_qty': abs(line.qty),
                        #         'state': 'draft',
                        #         'location_id': location_id if line.qty >= 0 else destination_id,
                        #         'location_dest_id': destination_id if line.qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                        #     })
                else:
                    moves |= Move.create({
                        'name': line.name,
                        'product_uom': line.uom_id.id, #line.product_id.uom_id.id,
                        'picking_id': order_picking.id if line.qty >= 0 else return_picking.id,
                        'picking_type_id': picking_type.id if line.qty >= 0 else return_pick_type.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': abs(line.qty),
                        'state': 'draft',
                        'location_id': location_id if line.qty >= 0 else destination_id,
                        'location_dest_id': destination_id if line.qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                    })

            # prefer associating the regular order picking, not the return
            order.write({'picking_id': order_picking.id or return_picking.id})

            if return_picking:
                order._force_picking_done(return_picking)
            if order_picking:
                order._force_picking_done(order_picking)

            # when the pos.config has no picking_type_id set only the moves will be created
            if moves and not return_picking and not order_picking:
                moves._action_assign()
                moves.filtered(lambda m: m.product_id.tracking == 'none')._action_done()

        return True

    # def create_composition_product(self, line, ddd, order_picking, return_picking, qty, picking_type, return_pick_type, location_id, destination_id):

    #     return {
    #             'name': line.name,
    #             'product_uom': line.uom_id.id, #ddd.uom_id.id,
    #             'picking_id': order_picking.id if ddd.product_quantity * qty >= 0 else return_picking.id,
    #             'picking_type_id': picking_type.id if ddd.product_quantity * qty >= 0 else return_pick_type.id,
    #             'product_id': ddd.product_id.id,
    #             'product_uom_qty': abs(ddd.product_quantity) * qty,
    #             'state': 'draft',
    #             'location_id': location_id if ddd.product_quantity * qty >= 0 else destination_id,
    #             'location_dest_id': destination_id if ddd.product_quantity * qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
    #         }




    def set_pack_operation_lot(self, picking=None):
        """Set Serial/Lot number in pack operations to mark the pack operation done."""

        StockProductionLot = self.env['stock.production.lot']
        PosPackOperationLot = self.env['pos.pack.operation.lot']
        has_wrong_lots = False
        for order in self:
            for move in (picking or self.picking_id).move_lines:
                picking_type = (picking or self.picking_id).picking_type_id
                lots_necessary = True
                if picking_type:
                    lots_necessary = picking_type and picking_type.use_existing_lots
                qty_done = 0
                pack_lots = []
                pos_pack_lots = PosPackOperationLot.search([('order_id', '=', order.id), ('product_id', '=', move.product_id.id)])

                if pos_pack_lots and lots_necessary:
                    for pos_pack_lot in pos_pack_lots:
                        stock_production_lot = StockProductionLot.search([('name', '=', pos_pack_lot.lot_name), ('product_id', '=', move.product_id.id)])
                        if stock_production_lot:
                            # a serialnumber always has a quantity of 1 product, a lot number takes the full quantity of the order line
                            qty = 1.0
                            if stock_production_lot.product_id.tracking == 'lot':
                                qty = abs(pos_pack_lot.pos_order_line_id.qty)
                            qty_done += qty
                            quant = stock_production_lot.quant_ids.filtered(lambda q: q.quantity > 0.0 and q.location_id.parent_path.startswith(move.location_id.parent_path))[-1:]
                            pack_lots.append({'lot_id': stock_production_lot.id, 'quant_location_id': quant.location_id.id, 'qty': qty})
                        else:
                            has_wrong_lots = True
                elif move.product_id.tracking == 'none' or not lots_necessary:
                    qty_done = move.product_uom_qty
                else:
                    move_line_lot = StockProductionLot.search([('product_id', '=', move.product_id.id)])
                    move_line_lot = move_line_lot.sorted(key=lambda r: r.removal_date).ids

                    st_move_line = move._get_move_lines()
                    st_move_line_q = st_move_line.filtered(lambda x: x.product_id.id == move.product_id.id)

                    for m_l_lot in st_move_line:
                        if m_l_lot.lot_id.id in move_line_lot:
                            if move.product_uom_qty == sum(st_move_line_q.mapped('product_uom_qty')):
                                m_l_lot.qty_done = m_l_lot.product_uom_qty
                            has_wrong_lots = False
                        else:
                            has_wrong_lots = True
                for pack_lot in pack_lots:
                    lot_id, quant_location_id, qty = pack_lot['lot_id'], pack_lot['quant_location_id'], pack_lot['qty']
                    self.env['stock.move.line'].create({
                        'picking_id': move.picking_id.id,
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                        'qty_done': qty,
                        'location_id': quant_location_id or move.location_id.id,
                        'location_dest_id': move.location_dest_id.id,
                        'lot_id': lot_id,
                    })
                if not pack_lots and not float_is_zero(qty_done, precision_rounding=move.product_uom.rounding):
                    if len(move._get_move_lines()) < 2:
                        move.quantity_done = qty_done
                    else:
                        move._set_quantity_done(qty_done)
        

        return has_wrong_lots

