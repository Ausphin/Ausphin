# -*- coding: utf-8 -*-

from odoo import fields, models, api

class CrmTeam(models.Model):
    _inherit = "crm.team"
    _order = "sequence, name"
    
    sequence = fields.Integer(string="Sequence")