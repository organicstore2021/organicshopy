"use strict";
/*
    License: OPL-1
    author: farooq@aarsol.com   
*/
odoo.define('pos_ticket.screens', function (require) {

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var _t = core._t;
    var gui = require('point_of_sale.gui');
    var qweb = core.qweb;

   
    screens.ReceiptScreenWidget.include({
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.back_order').click(function () {
                var order = self.pos.get_order();
                if (order) {
                    self.pos.gui.show_screen('products');
                }
            });
        },       
        show: function () {
            this._super();   
            try {

                
                var order = this.pos.get('selectedOrder');
                console.log(order)
                // console.log(this.pos.get_order())
                // console.log(order.get_total_with_tax())
                // console.log(order.get_total_tax())
                
                // console.log(this.pos.get_order().get_total_with_tax().toFixed(2)) 

                // var company_name = this.pos.get_order().pos.company.name
                // var company_vat = this.pos.get_order().pos.company.vat
                // var order_total_with_tax = order.get_total_with_tax().toFixed(2)
                // var order_total_tax = order.get_total_tax().toFixed(2)
                // var order_date =  new Intl.DateTimeFormat('en-US').format(new Date(this.pos.get_order().formatted_validation_date));
                // var order_time =  "11:20"; //new Intl.DateTimeFormat('en-US', {
                // //     hour: 'numeric', minute: 'numeric', second: 'numeric',
                // //     hour12: true,
                // //   }).format(new Date(this.pos.get_order().formatted_validation_date));

                
                // var QR_CODE = new QRCode("qrcode", {
                //     width: 300,
                //     height: 300,
                //     colorDark: "#000000",
                //     colorLight: "#ffffff",
                //     correctLevel: QRCode.CorrectLevel.H,
                //   });
                //   QR_CODE.makeCode(
                //       "اسم الشركة - Comapny Name" + "\n" + company_name + "\n" +
                //       "الرقم الضريبي للشركة - Company VAT number" + "\n" + company_vat + "\n" +
                //       "تاريخ الفاتورة - Receipt Date" + "\n" + order_date + "\n" +
                //       "زمن الفاتورة - Receipt Time" + "\n" + order_time + "\n" +
                //       "اجمالي الفاتروة شامل الضريبة - Total With Tax" + "\n" + order_total_with_tax + "\n" +
                //       "اجمالي الضريبة - Total Tax" + "\n" + order_total_tax + "\n" 
                //   );


                //   console.log("cccccc")
                // JsBarcode("#barcode", this.pos.get('selectedOrder').ean13, {
                //     format: "EAN13",
                //     displayValue: true,
                //     fontSize: 20
                // });
            } catch (error) {
                console.log(error)
            }
        },
        
    });

    

});
