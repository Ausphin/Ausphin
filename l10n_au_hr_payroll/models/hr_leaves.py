# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, time
from pytz import timezone

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    sick_leav = fields.Boolean(string="Sick Leave?", default=False)
    annual_leav = fields.Boolean(string="Annual Leave?", default=False)
    
