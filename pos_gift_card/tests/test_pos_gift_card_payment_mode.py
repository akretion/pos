# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.addons.gift_card.tests.common import TestGiftCardCommon
from odoo import fields

@tagged('post_install')
class TestPosGiftCardPaymentMode(TestGiftCardCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env.ref("product.product_product_3")
        cls.pos_config = cls.env.ref("point_of_sale.pos_config_main").copy()
        account_id = cls.env.company.account_default_pos_receivable_account_id
        cls.cash_payment_method = cls.env["pos.payment.method"].create(
            {
                "name": "Cash",
                "is_cash_count": True,
                "receivable_account_id": account_id.id,
                "cash_journal_id": cls.env["account.journal"]
                .search(
                    [("type", "=", "cash"), ("company_id", "=", cls.env.company.id)],
                    limit=1,
                )
                .id,
            }
        )
        cls.gift_card_payment_method = cls.env.ref("pos_gift_card.pos_payment_method_gift_card")

        cls.pos_config.write({'payment_method_ids': [(4, cls.gift_card_payment_method.id), (4, cls.cash_payment_method.id)]})

        cls.pos_config.open_session_cb()
        cls.session = cls.pos_config.current_session_id


        line_vals = {
            "name": "line",
            "product_id": cls.product.id,
            "qty": 1.0,
            "price_unit": 200,
            "price_subtotal": 200,
            "price_subtotal_incl": 200,
        }

        cls.order = cls.env["pos.order"].create(
            {
                "session_id": cls.session.id,
                "amount_tax": 0,
                "amount_total": 200,
                "amount_paid": 200,
                "amount_return": 0,
                "lines": [[0, 0, line_vals]],
            }
        )

        cls.order.add_payment(
            {
                "pos_order_id": cls.order.id,
                "amount": 100,
                "payment_date": fields.Date.today(),
                "payment_method_id": cls.cash_payment_method.id,
            }
        )


    def test_1_gift_card_with_code(self):
        self.order.add_payment(
            {
                "pos_order_id": self.order.id,
                "amount": 100,
                "payment_date": fields.Date.today(),
                "payment_method_id": self.cash_payment_method.id,
                "gift_card_with_code":True,
                "gift_card_amount":100 ,
                "gift_card_selected_id":self.gc1.id,
            }
        )

        self.order.action_pos_order_paid()

        self.assertEqual(len(self.gc1.gift_card_line_ids), 1)
        gc1_line = self.gc1.gift_card_line_ids[0]
        self.assertEqual(gc1_line.pos_order_id, self.order.id)
        self.assertEqual(gc1_line.amount_used, 100)


    def test_2_gift_card_with_partner(self):
        self.gc1.beneficiary_id = self.order.partner_id.id
        self.order.add_payment(
            {
                "pos_order_id": self.order.id,
                "amount": 100,
                "payment_date": fields.Date.today(),
                "payment_method_id": self.cash_payment_method.id,
                "gift_card_with_code":False,
                "gift_card_amount":100 ,
                "gift_card_selected_id":self.gc1.id,
            }
        )

        self.order.action_pos_order_paid()

        self.assertEqual(len(self.gc1.gift_card_line_ids), 1)
        gc1_line = self.gc1.gift_card_line_ids[0]
        self.assertEqual(gc1_line.pos_order_id, self.order.id)
        self.assertEqual(gc1_line.amount_used, 100)



