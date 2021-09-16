odoo.define("pos_ticket_without_price.OrderReceipt", function (require) {
    "use strict";

    const OrderReceipt = require("point_of_sale.OrderReceipt");
    const Registries = require("point_of_sale.Registries");

    const HidePriceOrderReceipt = (OrderReceipt) =>
        class extends OrderReceipt {
            isHidePrice() {
                return this.env.pos.hidePrice;
            }
        };
    Registries.Component.extend(OrderReceipt, HidePriceOrderReceipt);
    return OrderReceipt;
});
