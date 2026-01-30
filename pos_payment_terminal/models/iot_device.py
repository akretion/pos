import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class IoTDevice(models.Model):
    _name = 'iot.device'
    _inherit = ['iot.device', 'pos.load.mixin']

    # Add a type to distinguish payment terminals
    # type = fields.Selection(selection_add=[
    #     ('payment_terminal', 'Payment Terminal')
    # ], ondelete={'payment_terminal': 'set default'})

    # Caisse-AP specific protocol port (Default is usually 8888)
    tcp_port = fields.Integer(string="TCP Port", default=8888)

    @api.model
    def _load_pos_data_domain(self, data):
        # LOGGING HERE
        _logger.info("=============================================")
        _logger.info("POS LOADING: iot.device requested!")
        domain = [('active', '=', True)]
        count = self.search_count(domain)
        _logger.info(f"POS LOADING: Found {count} active devices in database.")
        _logger.info("=============================================")
        return domain

    @api.model
    def _load_pos_data_fields(self, config_id):
        """ Fields to expose to the POS JS """
        return ['id', 'name', 'ip', 'tcp_port', 'communication_system_id']#, 'type']
