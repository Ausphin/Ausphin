# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    body_action = fields.Html(
        related='company_id.body_action', string='Body Action')
    report_header = fields.Html(
        related='company_id.report_header', string='Report Header')
    report_footer = fields.Html(
        related='company_id.report_footer', string='Report Footer')
