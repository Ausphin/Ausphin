# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    body_action = fields.Html(string='Body Action')
    report_header = fields.Html(string='Report Header')
    report_footer = fields.Html(string='Report Footer')

    ani_body = fields.Html(string='Body')
    ani_header = fields.Html(string='Header')
    ani_footer = fields.Html(string='Footer')
