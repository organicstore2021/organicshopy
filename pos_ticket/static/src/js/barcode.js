odoo.define('custom_pos_barcode', function (require) {
    "use strict";

    var pos_screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var Model = require('web.DataModel');
    var new_pr = [];
    var core = require('web.core');
    var _t = core._t;




    pos_screens.PaymentScreenWidget.include({

        renderElement: function () {
            var self = this;
            this._super();



            this.$('.next').click(function () {
                JsBarcode("#barcode", self.old_order.name);


            });



        },

    });



});
