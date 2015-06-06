import logging
import openerp
from openerp.http import request

import werkzeug

from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

logger = logging.getLogger(__name__)


class WebsiteMaintenance(Website):

    def is_maintenance_mode(self):
        is_on = ['on', '1', 'true', 'yes']
        maintenance_mode = request.registry['ir.config_parameter'].get_param(
            request.cr, request.uid, 'website.maintenance_mode')
        logger.debug("maintenance_mode value: %s" % (maintenance_mode))
        if maintenance_mode in is_on:
            logger.info("Maintenance mode on")

            if not request.uid:
                logger.info("Not uid, request auth public")
                self._auth_method_public()

            allowed_group = request.env['ir.model.data'].sudo().get_object('base', 'group_website_designer')
            if allowed_group in request.env.user.groups_id:
                logger.info("Maintenance mode off for user_id: %s" % (request.env.user.id))
                return

            code=503
            status_message = request.registry['ir.config_parameter'].get_param(
                request.cr, request.uid, 'website.maintenance_message',
                "We're maintenance now")
            values = {
                'status_message': status_message,
                'status_code': code,
                'company_email': request.env.user.company_id.email
            }
            logger.debug(values)
            try:
                html = request.website._render('website_maintenance.%s' % code, values)
            except Exception:
                html = request.website._render('website.http_error', values)
            return werkzeug.wrappers.Response(html, status=code, content_type='text/html;charset=utf-8')

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        is_maintenance_mode = self.is_maintenance_mode()
        if not is_maintenance_mode:
            return super(WebsiteMaintenance, self).index()
        else:
            return is_maintenance_mode

    @http.route('/page/<page:page>', type='http', auth="public", website=True)
    def page(self, page, **opts):
        is_maintenance_mode = self.is_maintenance_mode()
        if not is_maintenance_mode:
            return super(WebsiteMaintenance, self).page(page)
        else:
            return is_maintenance_mode
