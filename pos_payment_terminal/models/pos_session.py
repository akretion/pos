from odoo import models, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        """ Tell Odoo to load the iot.device model into the POS JS """
        models = super()._load_pos_data_models(config_id)
        if 'iot.device' not in models:
            models.append('iot.device')
        return models
        #return ['iot.device']
