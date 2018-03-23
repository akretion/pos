/******************************************************************************
    Copyright (C) 2018 - Today: Akretion (https://www.akretion.com)
    @author: Raphaël Reverdy (https://akretion.com)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 *****************************************************************************/
odoo.define('pos_order_to_sale_order.state_machine', function (require) {
    "use strict";

    var stateMachine = { //State Machine
        listeners: [],
        allowed_states: [],
        // possible states : poso, draft, order, picking
        current: {
            name: 'poso',
            isPayable: true,
            isPosOrder: true,
            isPicking: true,
        },
        enter: function(target) {
            var next = {
                name: target
            };
            if (target == 'draft' ) {
                next.isPayable = false;
                next.isPosOrder = false;
                next.isPicking = false;
            }
            if (target == 'poso') {
                next.isPayable = true;
                next.isPosOrder = true;
                next.isPicking = true;
            }
            if (target == 'picking') {
                next.isPayable = true;
                next.isPosOrder = false;
                next.isPicking = true;
            }
            if (target == 'order') {
                next.isPayable = true;
                next.isPosOrder = false;
                next.isPicking = false;
            }
            this.notifiy(next);
        },
        exit: function(target) {
            var order = 'order';
            var possibles = [];
            var map = {};
            if (this.allowed_states.indexOf('order') == -1) {
                //order is not allowed, fallback to something else.
                possibles = this.allowed_states.filter(function (state) {
                    return state != target;
                }); //possibles = allowed_states - target - order
                order = possibles.shift(); //take first
            }
            map = {
                'poso': order,
                'order': 'poso',
                'picking': order,
                'draft': order
            };
            this.enter(map[target]);
        },
        toggle: function(target) {
            if (this.current.name == target){
                this.exit(target);
            } else {
                this.enter(target);
            }
        },
        notifiy: function(next) {
            var prev = this.current;
            this.current = next;
            this.listeners.forEach(function (cb) {
                cb(next, prev);
            }, this);
        }
    };
    window.stateMachine = stateMachine;
    return stateMachine;
});