/*
 *  Copyright 2021 Akretion
 *  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
 */
import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";

patch(PosStore.prototype, {
    add_new_order(data = {}) {
        // Set the previously used pricelist_id on the new order
        const order = this.get_order();
        const pricelist_id = order?.pricelist_id;
        const new_order = super.add_new_order(data);
        if (pricelist_id) {
            new_order.set_pricelist(pricelist_id);
        }
        return new_order;
    },
});
