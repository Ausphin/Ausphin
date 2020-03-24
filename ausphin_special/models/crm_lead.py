from odoo import models, fields, api, exceptions

class Lead(models.Model):
    _inherit = "crm.lead"
    
    team_id = fields.Many2one(comodel_name="crm.team",
        string="Journey",
        related="stage_id.team_id")