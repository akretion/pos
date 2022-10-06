/* Copyright 2022 Akretion (https://www.akretion.com)
 * @author Kévin Roche <kevin.roche@akretion.com>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("pos_gift_card.PaymentScreen", function(require) {
    "use strict";

    var PaymentScreen = require("point_of_sale.PaymentScreen");
    var Registries = require("point_of_sale.Registries");

    var GiftCardPaymentScreen = (PaymentScreen) =>
        class GiftCardPaymentScreen extends PaymentScreen {
            async _isOrderValid(isForceValidate) {
                var gift_card_id_list = []
                for (var paymentline in this.currentOrder.get_paymentlines()) {
                    var line = this.currentOrder.get_paymentlines()[paymentline]
                    if (line.payment_method.name == 'Gift Card' && !line.gift_card_selected_id) {
                        this.showPopup("ErrorPopup", {
                            title: this.env._t("No gift Card Selected"),
                            body: this.env._t(
                                "A gift Card is required for a payment."
                            ),
                        });
                        return false;
                    };
                    if (line.payment_method.name == 'Gift Card' && line.gift_card_amount != 0) {
                        gift_card_id_list.push(line.gift_card_selected_id.id)
                        if (line.amount > line.gift_card_selected_id.available_amount) {
                            this.showPopup("ErrorPopup", {
                                title: this.env._t("Wrong Gift Card Amount"),
                                body: this.env._t(
                                    "A Gift Card Amount is larger than the Available Amount."
                                ),
                            });
                            return false;
                        }
                    };
                }
                var check_duplicate_list = new Set(gift_card_id_list);
                if (gift_card_id_list.length !== check_duplicate_list.size) {
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("Only One Payment by Gift Card"),
                        body: this.env._t(
                            "A Gift Card can not be used several times in the same sale."
                        ),
                    });
                    return false;
                }
                return super._isOrderValid(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, GiftCardPaymentScreen);

    return PaymentScreen;
});
