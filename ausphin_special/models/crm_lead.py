# -*- coding: utf-8 -*-

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
    company_id = fields.Many2one(comodel_name="res.company",
        related="team_id.company_id",
        store=True)
    force_assign = fields.Boolean(string="Force Assign",
        related="stage_id.force_assign")
    is_user = fields.Boolean(string="Is User",
        compute="_compute_is_user")
    fees_and_guidelines = fields.Binary(string="Fees and Guidelines")
    fees_and_guidelines_fname = fields.Char(string="Fees and Guidelines Filename")
    skills_audit = fields.Binary(string="Skills Audit")
    skills_audit_fname = fields.Char(string="Skills Audit Filename")
    predeparture_checklist = fields.Binary(string="Pre-departure Checklist")
    predeparture_checklist_fname = fields.Char(string="Pre-departure Checklist Filename")
    nationality_id = fields.Many2one(comodel_name="res.country",
        string="Nationality",
        related="partner_id.x_studio_nationality")
    contact_name = fields.Char(required=True)
    mobile = fields.Char(required=True)
    partner_address_city = fields.Char(string="City",
        related="partner_id.city")
    partner_address_country_id = fields.Many2one(string="Country",
        comodel_name="res.country",
        related="partner_id.country_id")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("user_id")
    def _compute_is_user(self):
        for lead in self:
            lead.is_user = False
            if lead.user_id.id == self.env.uid:
                lead.is_user = True

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
        stage_obj = self.env["crm.stage"]
        stage_ids = stage_obj.search([]).ids
        current_stage_index = stage_ids.index(self.stage_id.id)
        if current_stage_index == (len(stage_ids) - 1):
            raise ValidationError("This is already the last stage!")
        next_stage_id = stage_ids[current_stage_index + 1]
        
        # get user to assign if force assign
        user_id = False;
        next_stage = stage_obj.browse(next_stage_id)
        if next_stage.force_assign:
            user_id = next_stage.sudo().get_assignee()
        
        self.sudo().write({
            "stage_id": next_stage_id,
            "user_id": user_id
        })
        return self.env.ref("crm.crm_lead_opportunities_tree_view").read()[0]
    
    def action_move_to_prev_stage(self):
        self.ensure_one()

        # get prev stage
        stage_ids = self.env["crm.stage"].search([]).ids
        current_stage_index = stage_ids.index(self.stage_id.id)
        if current_stage_index == 0:
            raise ValidationError("This is already the first stage!")
        prev_stage_id = stage_ids[current_stage_index - 1]
        
        # get last assigned user
        logs = self.stage_log_ids.filtered(lambda l: l.stage_id.id == prev_stage_id and
                                                     l.user_id)
        user_id = logs[-1].user_id.id if logs else False
        
        self.sudo().write({
            "stage_id": prev_stage_id,
            "user_id": user_id
        })
        return self.env.ref("crm.crm_lead_opportunities_tree_view").read()[0]

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
            if self._context.get("site_id"):
                value["site_id"] = self._context.get("site_id")
            if value:
                lead.write(value)
        return True