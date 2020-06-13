from odoo import http
from odoo.http import request
from odoo.addons.web_editor.controllers.main import Web_Editor



class Web_Editor_Extend(Web_Editor):

    @http.route(['/mass_mailing/snippets'], type='json', auth="user", website=True)
    def mass_mailing_snippet(self):
        values = {'company_id': request.env['res.users'].browse(request.uid).company_id,
        		'name': request.env['res.partner'].search([])}
        partner = {'name': request.env['res.partner'].search([])}
        return request.env.ref('mass_mailing.email_designer_snippets').render(values)