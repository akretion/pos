odoo.define("pos_ticket_without_price.ReceiptScreen", function (require) {
    "use strict";

    const ReceiptScreen = require("point_of_sale.ReceiptScreen");
    const Registries = require("point_of_sale.Registries");

    const HidePriceReceiptScreen = (ReceiptScreen) =>
        class extends ReceiptScreen {
            hidePrice() {
                // FIXME: global var
                this.env.pos.hidePrice = !this.env.pos.hidePrice;
                this.render();
            }
            isHidePrice() {
                return this.env.pos.hidePrice;
            }
        };
    Registries.Component.extend(ReceiptScreen, HidePriceReceiptScreen);
    return ReceiptScreen;
});
