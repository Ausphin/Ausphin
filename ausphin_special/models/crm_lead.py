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
        string="Service",
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
    citizenship_id = fields.Many2one(comodel_name="res.country",
        string="Citizenship",
        related="partner_id.citizenship_id")
    partner_address_city = fields.Char(string="City",
        related="partner_id.city")
    partner_address_country_id = fields.Many2one(string="Country",
        comodel_name="res.country",
        related="partner_id.country_id")
    scholarship_grant = fields.Float(string="Scholarship Grant (%)")
    is_scholar = fields.Boolean(string="Is Scholar Candidate")
    site_dependent = fields.Boolean(string="Site Dependent",
        related="stage_id.site_dependent")
    birth_date = fields.Date(string="Date of Birth",
        related="partner_id.birth_date")
    skills_audit_sched = fields.Datetime(string="Skills Audit Schedule")
    batch_num = fields.Char(string="Batch Number")
    class_start_date = fields.Date(string="Class Start Date")
    final_visume_url = fields.Char(string="Final Visume")
    is_visume_payed = fields.Boolean(string="Visume Payed")
    
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
        
        next_stage = self.get_next_stage(self.stage_id)
        user_id = False;
        if next_stage.force_assign:
            user_id = next_stage.sudo().get_assignee(site=self.site_id)
        
        self.sudo().write({
            "stage_id": next_stage.id,
            "user_id": user_id
        })
        return self.env.ref("crm.crm_lead_opportunities_tree_view").read()[0]
    
    def action_move_to_prev_stage(self):
        self.ensure_one()

        prev_stage = self.get_prev_stage(self.stage_id)
        logs = self.stage_log_ids.filtered(lambda l: l.stage_id.id == prev_stage.id and
                                                     l.user_id)
        user_id = logs[-1].user_id.id if logs else False
        
        self.sudo().write({
            "stage_id": prev_stage.id,
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
    
    def get_next_stage(self, stage):
        if stage.name == "Leads" and stage.team_id.name == "Enrollment" and self.is_scholar == False:
            enrollment_stage = stage.search([("name","=","Enrollment"),("team_id","=",self.team_id.id)])
            if not enrollment_stage:
                raise ValidationError("Enrollment stage not found!")
            return enrollment_stage[0]
        
        stage_ids = stage.search([]).ids
        current_stage_index = stage_ids.index(stage.id)
        if current_stage_index == (len(stage_ids) - 1):
            raise ValidationError("This is already the last stage!")
        return stage.browse(stage_ids[current_stage_index + 1])
    
    def get_prev_stage(self, stage):
        if stage.name == "Enrollment" and stage.team_id.name == "Enrollment" and self.is_scholar == False:
            leads_stage = stage.search([("name","=","Leads"),("team_id","=",self.team_id.id)])
            if not leads_stage:
                raise ValidationError("Leads stage not found!")
            return leads_stage[0]
        
        stage_ids = stage.search([]).ids
        current_stage_index = stage_ids.index(stage.id)
        if current_stage_index == 0:
            raise ValidationError("This is already the first stage!")
        prev_stage = stage.browse(stage_ids[current_stage_index - 1])
        return prev_stage