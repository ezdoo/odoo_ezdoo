#from openerp.osv import fields, osv
from openerp import models, fields, api

class website_maintenance_config_settings(models.Model):
    _inherit= 'website.config.settings'

    is_on = ['yes', 'true', '1', 'on']

    maintenance_mode = fields.Boolean('Enable Maintenance Mode')
    maintenance_message = fields.Char('Custom Maintenance Message')
    
    @api.cr_uid_ids_context
    def set_maintenance_mode(self, cr, uid, ids, context=None):
        config_param = self.pool.get('ir.config_parameter')
        config = self.browse(cr, uid, ids[0], context=context)
        if config.maintenance_mode:
            config_param.set_param(cr, uid,
                    'website.maintenance_mode', 'yes')
        else:
            config_param.set_param(cr, uid,
                    'website.maintenance_mode', 'no')

    @api.cr_uid_ids_context
    def set_maintenance_message(self, cr, uid, ids, context=None):
        config_param = self.pool.get('ir.config_parameter')
        config = self.browse(cr, uid, ids[0], context=context)
        maintenance_message = config.maintenance_message
        print type(maintenance_message)
        if maintenance_message not in ['', False]:
            config_param.set_param(cr, uid,
                'website.maintenance_message', maintenance_message)

    @api.cr_uid_ids_context
    def get_default_maintenance_mode(self, cr, uid, ids, fields, context=None):
        config_param = self.pool.get('ir.config_parameter')
        maintenance_param = config_param.get_param(cr, uid,
                    'website.maintenance_mode')
        
        if maintenance_param in self.is_on:
            maintenance_mode = True
        else:
            maintenance_mode = False

        return {'maintenance_mode': maintenance_mode}

    @api.cr_uid_ids_context
    def get_default_maintenance_message(self, cr, uid, ids, fields, context=None):
        config_param = self.pool.get('ir.config_parameter')
        maintenance_message = config_param.get_param(cr, uid,
                    'website.maintenance_message', '')

        return {'maintenance_message': maintenance_message}
