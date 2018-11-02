# coding: utf-8
# @author: Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError
from odoo.tools import float_is_zero


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    statement_ids = fields.One2many(
        'account.bank.statement.line',
        'pos_so_statement_id', string='Pos Payments',
        states={'draft': [('readonly', False)]}, readonly=True)

    @api.model
    def _prepare_order_from_pos(self, order_data):
        res = super(SaleOrder, self)._prepare_order_from_pos(order_data)
        if not order_data['partner_id']:
            pos_session = self.env['pos.session'].browse(
                order_data['pos_session_id'])
            partner_id = pos_session.config_id.anonymous_partner_id
            if not partner_id:
                raise UserError(
                    "There is no anonymous partner defined for the Pos '%s'.\n"
                    "Please add it."
                    % pos_session.config_id.name)
            res['partner_id'] = partner_id.id
            pricelist_id = partner_id.property_product_pricelist
            if not pricelist_id:
                pricelist_id = pos_session.config_id.pricelist_id
            res['pricelist_id'] = pricelist_id.id,
        return res

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        res = super(SaleOrder, self)._prepare_invoice()
        pos_anonym_journal = self.env.context.get(
            'pos_anonym_journal', False)
        if pos_anonym_journal:
            res['journal_id'] = pos_anonym_journal.id
        res['session_id'] = self.session_id.id
        if self.session_id and self.partner_id == self.env.ref(
                'pos_order_to_sale_order.res_partner_anonymous'):
            res['pos_anonyme_invoice'] = True
        return res

    @api.model
    def _payment_fields(self, ui_paymentline):
        return {
            'amount': ui_paymentline['amount'] or 0.0,
            'payment_date': ui_paymentline['name'],
            'statement_id': ui_paymentline['statement_id'],
            'payment_name': ui_paymentline.get('note', False),
            'journal': ui_paymentline['journal_id'],
        }

    @api.model
    def create_order_from_pos(self, order_data):
        res = super(SaleOrder, self).create_order_from_pos(order_data)
        prec_acc = self.env['decimal.precision'].precision_get('Account')
        order = self.browse(res.get('sale_order_id', False))
        session = self.env['pos.session'].browse(
            order_data['pos_session_id'])

        if session.state == 'closing_control' or session.state == 'closed':
            raise UserError(
                u"La session '%s' du PdV est close.\n"
                "Please close it and restart it. "
                "If you want to make another sale "
                % session.name)
        journal_ids = set()

        payments = order_data.get('statement_ids', []) or []
        for payment in payments:
            if payment:
                self.add_payment(
                    order.id, self._payment_fields(payment[2]))
                journal_ids.add(payment[2]['journal_id'])

        if session.sequence_number <= order_data['sequence_number']:
            session.write(
                {'sequence_number': order_data['sequence_number'] + 1})
            session.refresh()

        if payments and not float_is_zero(
                order_data['amount_return'], prec_acc):
            cash_journal = session.cash_journal_id
            if not cash_journal:
                # Select for change one of the cash
                # journals used in this payment
                cash_journals = self.env['account.journal'].search([
                    ('type', '=', 'cash'),
                    ('id', 'in', list(journal_ids)),
                ], limit=1)
                if not cash_journals:
                    # If none, select for change one of
                    # the cash journals of the POS
                    # This is used for example when
                    # a customer pays by credit card
                    # an amount higher than total amount
                    # of the order and gets cash back
                    cash_journals = [
                        statement.journal_id for statement
                        in session.statement_ids
                        if statement.journal_id.type == 'cash']
                    if not cash_journals:
                        raise UserError(
                            _("No cash statement found for this session."
                              " Unable to record returned cash."))
                cash_journal = cash_journals[0]
            self.add_payment(order.id, {
                'amount': -order_data['amount_return'],
                'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'payment_name': _('return'),
                'journal': cash_journal.id,
            })
        return res

    @api.multi
    def _prepare_payment_vals(self, order_id, data):
        context = dict(self._context or {})
        property_obj = self.env['ir.property']
        order = self.env['sale.order'].browse(order_id)
        args = {
            'amount': data['amount'],
            'date': data.get('payment_date', time.strftime('%Y-%m-%d')),
            'name': order.name + ': ' + (data.get('payment_name', '') or ''),
            'partner_id': order.partner_id and (
                self.env['res.partner']._find_accounting_partner(
                    order.partner_id).id or False),
        }
        account_def = property_obj.get('property_account_receivable_id',
                                       'res.partner')
        args['account_id'] = ((
            order.partner_id and
            order.partner_id.property_account_receivable_id and
            order.partner_id.property_account_receivable_id.id) or
            (account_def and account_def.id) or False)

        if not args['account_id']:
            if not args['partner_id']:
                msg = _('There is no receivable account defined '
                        'to make payment.')
            else:
                msg = _('There is no receivable account defined '
                        'to make payment for the partner: "%s" (id:%d).') % (
                            order.partner_id.name, order.partner_id.id,)
            raise UserError(_('Configuration Error!'), msg)

        context.pop('pos_session_id', False)

        journal_id = data.get('journal', False)
        statement_id = data.get('statement_id', False)
        if not(journal_id or statement_id):
            raise UserError(
                "No statement_id or journal_id passed to the method!")

        for statement in order.statement_ids:
            if statement.id == statement_id:
                journal_id = statement.journal_id.id
                break
            elif statement.journal_id.id == journal_id:
                statement_id = statement.statement_id.id
                break

        if not statement_id:
            raise UserError(_('Error!'),
                            _('You have to open at least one cashbox.'))

        args.update({
            'statement_id': statement_id,
            'journal_id': journal_id,
            'pos_so_statement_id': order_id,
            'ref': order.session_id.name,
            'sale_ids': [(6, 0, [order_id])]
        })
        return args

    @api.multi
    def add_payment(self, order_id, data):
        """Create a new payment for the order"""
        statement_line_obj = self.env['account.bank.statement.line']
        args = self._prepare_payment_vals(order_id, data)
        return statement_line_obj.create(args)
