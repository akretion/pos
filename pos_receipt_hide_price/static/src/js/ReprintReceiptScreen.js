odoo.define("pos_receipt_hide_price.ReprintReceiptScreen", function (require) {
    "use strict";

    const ReprintReceiptScreen = require("point_of_sale.ReprintReceiptScreen");
    const Registries = require("point_of_sale.Registries");

    const HidePriceReprintReceiptScreen = (ReprintReceiptScreen) =>
        class extends ReprintReceiptScreen {
            hidePrice() {
                // FIXME: global var
                this.env.pos.hidePrice = !this.env.pos.hidePrice;
                this.render();
            }
            isHidePrice() {
                return this.env.pos.hidePrice;
            }
        };
    Registries.Component.extend(ReprintReceiptScreen, HidePriceReprintReceiptScreen);
    return ReprintReceiptScreen;
});
