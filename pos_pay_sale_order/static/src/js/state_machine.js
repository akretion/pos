/******************************************************************************
    Copyright (C) 2018 - Today: Akretion (https://www.akretion.com)
    @author: Raphaël Reverdy (https://akretion.com)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 *****************************************************************************/

odoo.define('pos_pay_sale_order.state_machine', function (require) {
    "use strict";
    var stateMachine = require('pos_order_to_sale_order.state_machine');
    stateMachine.allowPayment = true;
});
