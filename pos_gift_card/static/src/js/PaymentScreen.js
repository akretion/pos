/* Copyright 2022 Akretion (https://www.akretion.com)
 * @author Kévin Roche <kevin.roche@akretion.com>
 * @author Raphaël Reverdy <raphael.reverdy@akretion.com>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("pos_gift_card.PaymentScreen", function(require) {
    "use strict";

    var PaymentScreen = require("point_of_sale.PaymentScreen");
    var Registries = require("point_of_sale.Registries");

    var GiftCardPaymentScreen = (PaymentScreen) =>
        class GiftCardPaymentScreen extends PaymentScreen {
            async _isOrderValid(isForceValidate) {

                var has_error = this.currentOrder.get_paymentlines().filter( (paymentLine) => {
                    return paymentLine.payment_method.is_gift_card
                }).some( (paymentLine) => {
                    if (!paymentLine.gift_card_id) {
                        this.showPopup("ErrorPopup", {
                            title: this.env._t("No gift Card Selected"),
                            body: this.env._t(
                                "Gift card not configured."
                            ),
                        });
                        return true;
                    };

                    if (paymentLine.amount > paymentLine.gift_card_available_amount) {
                        this.showPopup("ErrorPopup", {
                            title: this.env._t("Wrong Gift Card Amount"),
                            body: this.env._t(
                                "A Gift Card Amount is larger than the Available Amount."
                            ),
                        });
                        return true;
                    }
                });
                if (has_error) {
                    //stop
                    return false;
                }
                return super._isOrderValid(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, GiftCardPaymentScreen);

    return PaymentScreen;
});
