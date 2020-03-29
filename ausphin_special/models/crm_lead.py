from odoo import models, fields, api 
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.lead"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    stage_id = fields.Many2one(comodel_name="crm.stage",
        domain=False)
    team_id = fields.Many2one(comodel_name="crm.team",
        string="Journey",
        related="stage_id.team_id",
        store=True)
    user_id = fields.Many2one(comodel_name="res.users",
        string="Assigned To",
        domain="[('stage_ids','in',[stage_id])]")
    
    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################
    

    #########################
    # CRUD method overrides #
    #########################
    
    
    ##################
    # Action methods #
    ##################
    def action_move_to_next_stage(self):
        self.ensure_one()

        # get next stage
        stage_ids = self.env["crm.stage"].sudo().search([]).ids
        current_stage_index = stage_ids.index(self.stage_id.id)
        if current_stage_index == (len(stage_ids) - 1):
            raise ValidationError("This is already the last stage!")
        next_stage_id = stage_ids[current_stage_index + 1]

        self.write({
            "stage_id": next_stage_id,
            "user_id": False
        })
        return True
    
    def action_move_to_prev_stage(self):
        self.ensure_one()

        # get prev stage
        stage_ids = self.env["crm.stage"].sudo().search([]).ids
        current_stage_index = stage_ids.index(self.stage_id.id)
        if current_stage_index == 0:
            raise ValidationError("This is already the first stage!")
        prev_stage_id = stage_ids[current_stage_index - 1]
        
        # get last assigned user
        logs = self.stage_log_ids.filtered(lambda l: l.stage_id.id == prev_stage_id and
                                                     l.user_id)
        user_id = logs[-1].user_id.id if logs else False
        
        self.write({
            "stage_id": prev_stage_id,
            "user_id": user_id
        })
        return True

    ####################
    # Business methods #
    ####################
    def allocate_salesman(self, user_ids=None, team_id=False):
        index = 0
        for lead in self:
            value = {}
            if team_id:
                value["team_id"] = team_id
            if user_ids:
                value["user_id"] = user_ids[index]
                # Cycle through user_ids
                index = (index + 1) % len(user_ids)
            if self._context.get("stage_id"):
                value["stage_id"] = self._context.get("stage_id")
            if value:
                lead.write(value)
        return True