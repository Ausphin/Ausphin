from odoo import models, fields, api, exceptions

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
    team_id = fields.Many2one(comodel_name="crm.team",
        string="Journey",
        related="stage_id.team_id",
        store=True)
    
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