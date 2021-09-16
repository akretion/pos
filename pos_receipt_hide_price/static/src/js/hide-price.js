odoo.define("pos_ticket_without_price.ReceiptScreen", function (require) {
    "use strict";

    const ReceiptScreen = require("point_of_sale.ReceiptScreen");
    const Registries = require("point_of_sale.Registries");

    const HidePriceReceiptScreen = (ReceiptScreen) =>
        class extends ReceiptScreen {
            hidePrice() {
                // ...
            }
        };
    Registries.Component.extend(ReceiptScreen, HidePriceReceiptScreen);
    return ReceiptScreen;
});
