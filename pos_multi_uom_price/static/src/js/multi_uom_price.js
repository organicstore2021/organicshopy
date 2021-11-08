odoo.define('pos.multi_uom_price', function (require) {
"use strict";

	var screens = require('point_of_sale.screens');
	var models = require('point_of_sale.models');
	var core = require('web.core');

	var QWeb = core.qweb;
	var rpc = require('web.rpc');

	var _super_orderline = models.Orderline.prototype;
	var SuperPosModel = models.PosModel;


	models.load_models({
		label:  'product.template',
		loaded: function(self){
			  rpc.query({
				  model:'product.template',
				  method:'get_data',
				  args:[self.config.picking_type_id]
			  })
		  .then(function(result) {
			self.multi_uom = result
		  });
		}
	});

	

	models.Orderline = models.Orderline.extend({
		initialize: function(attr, options) {
			_super_orderline.initialize.call(this,attr,options);
			if (options.json) {
				if (this.uom_id){
					return;
				} else {
					this.uom_id = this.product.uom_id;
					return;
				}
			}
			this.uom_id = options.product.uom_id;
		},
		get_unit: function(){
			if (this.uom_id){
				var unit_id = this.uom_id;
			}else{
				var unit_id = this.product.uom_id;
			}
			if(!unit_id){
				return undefined;
			}
			unit_id = unit_id[0];
			if(!this.pos){
				return undefined;
			}
			return this.pos.units_by_id[unit_id];
		},
		set_uom: function(uom_id){
			this.order.assert_editable();
			this.uom_id = uom_id;
			this.trigger('change',this);
		},
		export_as_JSON: function(){
			var json = _super_orderline.export_as_JSON.call(this);
			json.uom_id = this.uom_id[0];
			return json;
		},
		init_from_JSON: function(json){
			_super_orderline.init_from_JSON.apply(this,arguments);
			this.uom_id = {0:this.pos.units_by_id[json.uom_id].id, 1:this.pos.units_by_id[json.uom_id].name};
			this.price_manually_set = true;
		},
	});


	var UOMButton = screens.ActionButtonWidget.extend({
		template: 'UOMButton',
		button_click: function(){
			
			var list = [];
			var price = [];
			var line = this.pos.get_order().get_selected_orderline();
			if (line) {
				console.log(".........................", line.pos.multi_uom)
				var uom = line.pos.multi_uom[line.product.product_tmpl_id];
				
				if (uom) 
				{
					_.each(uom, function(u) {
						list.push({label:line.pos.units_by_id[u['id']].display_name + '      [' + u['price'] + ']' + '      [' + u['barcode'] + ']', item:u['id'] });
						price[u['id']] = u['price'];
					});

					this.gui.show_popup('selection',{
						title: 'UOM',
						list: list,
						confirm: function (uom_id) {
							line.set_unit_price(price[uom_id]);
							line.price_manually_set = true;
							uom_id = {0:line.pos.units_by_id[uom_id].id, 1:line.pos.units_by_id[uom_id].name};
							line.set_uom(uom_id);
							
						},
					});
				}
			}
		},
	});


	models.PosModel = models.PosModel.extend({
  
		scan_product: function(parsed_code) {  
			var self = this;
			var result = SuperPosModel.prototype.scan_product.call(this, parsed_code)
			var uom = self.multi_uom
			if (!result) 
			{
				if (uom) 
				{
					_.each(uom, function(u) {
						_.each(u, function(uu) {
							if(parsed_code.base_code == uu['barcode']){
								console.log(self.units_by_id[uu['id']])
								self.get_order().add_product(self.db.product_by_id[uu['product_id']], {
									scan: true,
									price: uu['price'], 
								});

								result = true
								
								
								var line = self.get_order().get_selected_orderline();
								line.set_uom({0:self.units_by_id[uu['id']].id, 1:self.units_by_id[uu['id']].name});
							}
						});
					});
				}
				
			}


			return result;
		}
	});

	screens.define_action_button({
		'name': 'uom',
		'widget': UOMButton,
	});

});
