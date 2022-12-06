/* Copyright 2022 Akretion (https://www.akretion.com)
 * @author Kévin Roche <kevin.roche@akretion.com>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("pos_gift_card.models", function (require) {
  "use strict";

  const models = require("point_of_sale.models");

    var _paymentlinegiftcard = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        initialize: function () {
            _paymentlinegiftcard.initialize.apply(this, arguments);
            this.gift_card_selected_id = null;
            this.gift_card_amount = null;
            this.gift_card_with_code = null;
        },
        init_from_JSON: function (json) {
            _paymentlinegiftcard.init_from_JSON.apply(this, arguments);
            this.gift_card_selected_id = json.gift_card_selected_id;
            this.gift_card_amount = json.gift_card_amount;
            this.gift_card_with_code = json.gift_card_with_code;
        },
        export_as_JSON: function () {
            var vals = _paymentlinegiftcard.export_as_JSON.apply(this, arguments);
            vals.gift_card_selected_id = this.gift_card_selected_id;
            vals.gift_card_amount = this.gift_card_amount;
            vals.gift_card_with_code = this.gift_card_with_code;
            return vals;
        },
    });

  models.load_fields("pos.payment.method",['is_gift_card'])
  
  models.load_models([
    {
      model: "gift.card",
      fields: ["code", "available_amount", "state", "is_divisible", "name", "beneficiary_id"],
      loaded: function (self, giftCard) {
        self.giftCard = giftCard;
    },
    },
  ]);
});
