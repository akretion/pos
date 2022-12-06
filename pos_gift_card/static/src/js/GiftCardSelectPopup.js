odoo.define('point_of_sale.GiftCardSelectPopup', function (require) {
    'use strict';

    const { useState } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class GiftCardSelectPopup extends AbstractAwaitablePopup {

        constructor() {
            super(...arguments);
            this.state = useState({ selectedId: this.props.list.find((item) => item.isSelected) });
        }
        selectItem(itemId) {
            this.state.selectedId = itemId;
            this.confirm();
        }
        /**
         * We send as payload of the response the selected item.
         *
         * @override
         */
        getPayload() {
            var selected = this.props.list.find((item) => this.state.selectedId === item.id);
            var code = this.state.inputValue;
            if (selected && selected.item) {
                var method = "list";
            } else {
                var method = "code";
            }
            return { 
                "method": method,
                "code": code,
                "list": selected.item
            };
        }
    }
    GiftCardSelectPopup.template = 'GiftCardSelectPopup';
    GiftCardSelectPopup.defaultProps = {
        confirmText: 'Confirm',
        cancelText: 'Cancel',
        title: 'Select',
        body: '',
        list: [],
    };

    Registries.Component.add(GiftCardSelectPopup);

    return GiftCardSelectPopup;
});
