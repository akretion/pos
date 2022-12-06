/* Copyright 2022 Akretion (https://www.akretion.com)
 * @author Kévin Roche <kevin.roche@akretion.com>
 * @author Raphaël Reverdy <raphael.reverdy@akretion.com>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('pos_gift_card.PaymentScreenPaymentLines', function(require) {
    'use strict';

    const PaymentScreenPaymentLines = require('point_of_sale.PaymentScreenPaymentLines');
    const Registries = require('point_of_sale.Registries');

    var PosGiftcardPaymentLines = (PaymentScreenPaymentLines) =>
        class PosGiftcardPaymentLines extends PaymentScreenPaymentLines {
            get currentOrder() {
                return this.env.pos.get_order();
            }
            get selectedPaymentLine() {
                return this.currentOrder.selected_paymentline;
            }

            async giftcardconfigure() {
                this.giftcardPartnerOrCode();
            }

            async validateCode(code) {
                var giftCard = await this.rpc({
                    model: "gift.card",
                    method: "search_read",
                    domain: [
                        ["code", "=", code], ["state", "=", "active"]
                    ],
                    fields: ["name", "code", "available_amount", "is_divisible"],
                });
                if (!giftCard) { 
                    return; 
                } else {
                    return giftCard[0];
                }
            }

            applyGiftcard(paymentLine, giftcard) {
                paymentLine.gift_card_id = giftcard.id
                paymentLine.amount = Math.min(
                    giftcard.available_amount,
                    paymentLine.order.get_due(paymentLine)
                );
            }

            async giftcardPartnerOrCode(){
                var currentClient = this.currentOrder.get_client();
                var giftCardList = [];

                if (currentClient) {
                    let giftCards = await this.rpc({
                        model: "gift.card",
                        method: "search_read",
                        domain: [
                            ["beneficiary_id", "=", currentClient.id],
                            ["state", "=", "active"]
                        ],
                        fields: ["name", "available_amount", "is_divisible"],
                    });

                    giftCardList = giftCards.map(gift => ({
                        id: gift.id,
                        label: gift.name + " - " + gift.available_amount,
                        isSelected: gift.id === this.selectedPaymentLine.gift_card_id,
                        item: gift,
                    }));
                }

                const { confirmed, payload } = await this.showPopup(
                    'GiftCardSelectPopup',
                    {
                        title: this.env._t('Select or enter a gift card'),
                        list: giftCardList,
                    }
                );
                if (confirmed) {
                    if (payload.method == "code") {
                        if (payload.code) {
                            var giftcard = await this.validateCode(payload.code);
                        }
                        if (!payload.code || !giftcard) {
                            const { confirmed } = await this.showPopup("ErrorPopup", {
                                title: this.env._t("Wrong Gift Card Code"),
                                body: this.env._t(
                                    "Please retry"
                                ),
                            });
                            if (confirmed) {
                                this.giftcardconfigure()
                            }                            
                        }
                    } else {
                        var giftcard = payload.list;
                    }
                    if (giftcard) {
                        this.applyGiftcard(this.selectedPaymentLine, giftcard);
                        this.trigger('select-payment-line', this.selectedPaymentLine);
                    }
                }
            };
    }
    Registries.Component.extend(PaymentScreenPaymentLines, PosGiftcardPaymentLines);

    return PosGiftcardPaymentLines;
});
