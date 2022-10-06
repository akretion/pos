/* Copyright 2022 Akretion (https://www.akretion.com)
 * @author Kévin Roche <kevin.roche@akretion.com>
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
            if (this.currentOrder.get_client()) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Gift Card'),
                        body: this.env._t('Choose a Gift Card by:'),
                        cancelText: this.env._t('Partner'),
                        confirmText: this.env._t('Code'),
                });
                if (confirmed) {
                    this.giftcardcode();
                } else {
                    this.giftcardpartner();
                }
            } else {
                this.giftcardcode();
            }
        }


        /*BY CODE*/
        async giftcardcode(){
            const { confirmed, payload: code } = await this.showPopup('TextInputPopup', {
                title: this.env._t('Enter Gift Card Code'),
                startingValue: '',
            });
            if (confirmed && code !== '') {
                var giftCard = await this.rpc({
                    model: "gift.card",
                    method: "search_read",
                    domain: [
                        ["code", "=", code], ["state", "=", "active"]
                    ],
                    fields: ["name", "code", "available_amount", "is_divisible"],
                });
                if (giftCard.length) {
                    this.selectedPaymentLine.gift_card_selected_id = giftCard[0]
                    this.selectedPaymentLine.gift_card_with_code = true;
                } else {
                    const { confirmed } = await this.showPopup("ErrorPopup", {
                        title: this.env._t("Wrong Gift Card Code"),
                        body: this.env._t(
                            "Please retry"
                        ),
                    });
                    if (confirmed && code !== '') {
                        this.giftcardconfigure()
                    }
                }
            }
        };

        /*BY PARTNER*/
        async giftcardpartner(){
            var currentClient = this.currentOrder.get_client();
            var giftCards = await this.rpc({
                model: "gift.card",
                method: "search_read",
                domain: [
                    ["beneficiary_id", "=", currentClient.id],
                    ["state", "=", "active"]
                ],
                fields: ["name", "available_amount", "is_divisible"],
            });

            let giftCardList = [];
            let gifts = giftCards.map(gift => ({
                id: gift.id,
                label: gift.name + " - " + gift.available_amount,
                isSelected: gift.id === this.selectedPaymentLine.gift_card_selected_id,
                item: gift,
            }));
            giftCardList = giftCardList.concat(gifts);


            const { confirmed, payload: giftCard } = await this.showPopup(
                'SelectionPopup',
                {
                    title: this.env._t('Select the gift card'),
                    list: giftCardList,
                }
            );
            if (confirmed) {
                this.selectedPaymentLine.gift_card_selected_id = giftCard
                this.selectedPaymentLine.gift_card_with_code = false;
            }
        };

}
    Registries.Component.extend(PaymentScreenPaymentLines, PosGiftcardPaymentLines);

    return PosGiftcardPaymentLines;
});
