# -*- coding: utf-8 -*-

from openerp import models, fields, api


class website_custom_assets(models.Model):
    _inherit = 'website'

    custom_assets_stylesheets = fields.Text('Stylesheets Assets')
    custom_assets_javascripts = fields.Text('Javascripts Assets')

    @api.cr_uid_ids_context
    def get_custom_assets(self, cr, uid, ids, context=None):
        read_fields = ["custom_assets_stylesheets", "custom_assets_javascripts"]
        assets = self.read(cr, uid, ids, read_fields, context=context)
        return assets


class website_custom_assets_config_settings(models.TransientModel):
    _inherit = 'website.config.settings'

    custom_assets_stylesheets = fields.Text('Stylesheets Assets', related='website_id.custom_assets_stylesheets')
    custom_assets_javascripts = fields.Text('Javascripts Assets', related='website_id.custom_assets_javascripts')
