# -*- coding: utf-8 -*-
# © 2018 Akretion
# @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
import openerp.addons.decimal_precision as dp
from odoo.exceptions import Warning as UserError
from odoo.tools import float_is_zero


class PayPosSaleOrder(models.TransientModel):
    _name = 'pay.pos.sale.order'
    _description = 'Wizard to generate a banck statement payment from'
    'the sale order created by pos'


    @api.model
    def _get_statement_domain(self):
        so = self.env['pos.session']
        order_id = self.env.context.get('active_id')
        if not order_id:
            return [('id', '=', False)]
        sessions = so.search(
            [('state', '=', 'opened'), ('user_id', '=', self.env.uid)])
        if sessions:
            return [('id', 'in', sessions[0].statement_ids.ids)]
        else:
            raise UserError(
                _('There is no pos session opened.'))

    @api.model
    def _default_statement_id(self):
        so = self.env['pos.session']
        order_id = self.env.context.get('active_id')
        if not order_id:
            return self.env['account.bank.statement']
        sessions = so.search(
            [('state', '=', 'opened'), ('user_id', '=', self.env.uid)])
        if sessions:
            cash_statement = False
            for st in sessions[0].statement_ids:
                if st.journal_id.type == 'cash':
                    cash_statement = st
                    return cash_statement
            # for journal in sessions[0].journal_ids:
            #     if journal.type == 'cash':
            #         cash_journal = journal
            #         return cash_journal
            # if not cash_statement:
            #     raise UserError(
            #         _('The session %s, do not contains cash statement opened.'
            #           % sessions[0].name))
        else:
            raise UserError(
                _('There is no pos session opened.'))

    @api.model
    def _default_amount(self):
        order_id = self.env.context.get('active_id')
        if not order_id:
            return 0
        order = self.env['sale.order'].browse(order_id)
        amount_payed = sum([st.amount for st in order.statement_ids])
        amount_to_paye = order.amount_total - amount_payed
        prec_acc = self.env['decimal.precision'].precision_get('Account')
        if float_is_zero(amount_to_paye, prec_acc):
            raise UserError(
                _('Error!') + 
                _('No thing to pay. Order is yet payed or it amount is 0'))
        return amount_to_paye

    statement_id = fields.Many2one(
        'account.bank.statement', domain=_get_statement_domain,
        #  default=_default_statement_id,
         )
    amount = fields.Float('Amount', digits=dp.get_precision('Sale Price'),
                          default=_default_amount)
    date = fields.Datetime('Payment Date', default=fields.Datetime.now)
    description = fields.Char('Description', size=64)

    @api.multi
    def pay_sale_order(self):
        """ Pay the sale order """
        self.ensure_one()
        if len(self.env.context.get('active_ids', [])) > 1:
            raise UserError(
                _('Error!'),
                _('You can pay only one order .'))
        order_id = self.env.context.get('active_id')
        payment_data = {
            'amount': self.amount,
            'payment_date': self.date,
            'statement_id': self.statement_id.id,
            'payment_name': self.description,
            'journal': self.statement_id.journal_id.id,
        }
        order = self.env['sale.order'].browse(order_id)
        order.add_payment(payment_data)
        session = order.session_id
        if not session:
            uid = self.env.context.get('uid')
            session = self.env['pos.session'].search([
                ('state', '=', 'opened'), ('user_id', '=', uid)], limit=1)
            if not session:
                raise UserError(
                    u"Il n'y a pas de session de PdV ouverte avec votre "
                    u"utilisateur.\nVeuillez en ouvrir une pour poursuivre.")
        invoice = session._generate_invoice(
            partner_id=order.partner_id.id,
            grouped=True, anonym_order=False, anonym_journal=True,
            orders=order)
        order.session_id._reconcile_invoice_with_pos_payment(
            invoice)
        return True

    @api.multi
    def pay_sale_order_and_confirm(self):
        """ Pay the sale order """
        self.ensure_one()
        self.pay_sale_order()
        order = self.env['sale.order'].browse(
            self.env.context.get('active_id'))
        return order.action_button_confirm()
