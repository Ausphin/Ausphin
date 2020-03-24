# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = "crm.lead"
    
    def action_move_to_next_stage(self):
        self.ensure_one()
        stage_ids = self.env["crm.stage"].sudo().search([]).ids
        current_stage_index = stage_ids.index(self.stage_id.id)
        if current_stage_index == (len(stage_ids) - 1):
            raise ValidationError("This is already the last stage!")
        return self.write({"stage_id": stage_ids[current_stage_index + 1]})
        
    def action_move_to_prev_stage(self):
        self.ensure_one()
        stage_ids = self.env["crm.stage"].sudo().search([]).ids
        current_stage_index = stage_ids.index(self.stage_id.id)
        if current_stage_index == 0:
            raise ValidationError("This is already the first stage!")
        return self.write({"stage_id": stage_ids[current_stage_index - 1]})