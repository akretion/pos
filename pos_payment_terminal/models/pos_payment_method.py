from odoo import fields, models

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    iot_device_id = fields.Many2one(
        'iot.device',
        string='Payment Terminal',
#        domain="[('type', '=', 'payment_terminal')]",
        help="Select the specific Payment Terminal device for this method."
    )

    def _get_payment_terminal_selection(self):
        """ Adds the option to the 'Use a Payment Terminal' selection """
        selection = super()._get_payment_terminal_selection()
        selection.append(('caisse_ap', 'Ingenico (Caisse-AP / Direct Socket)'))
        return selection

    def _load_pos_data_fields(self, config_id):
        """ Add iot_device_id to the fields loaded in POS JS """
        fields = super()._load_pos_data_fields(config_id)
        fields.append('iot_device_id')
        return fields
