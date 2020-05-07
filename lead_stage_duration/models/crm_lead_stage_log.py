# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api

SECONDS_IN_A_DAY = 60 * 60 * 24

class CrmLeadStageLog(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.lead.stage.log"
    _description = "Log of stage change"
    
    ###################
    # Default methods #
    ###################
  
        
    ######################
    # Fields declaration #
    ######################
    start_date = fields.Datetime(string="Start Date",
        required=True)
    end_date = fields.Datetime(string="End Date")
    actual_duration = fields.Float(string="Running Duration",
        compute="_compute_actual_duration")
    actual_duration_text = fields.Char(string="Approx. Duration",
        compute="_compute_actual_duration")
    user_id = fields.Many2one(string="Assignee",
        comodel_name="res.users")
    stage_id = fields.Many2one(string="Stage",
        comodel_name="crm.stage",
        required=True)
    lead_id = fields.Many2one(string="Lead/Opportunity",
        comodel_name="crm.lead",
        required=True,
        ondelete="cascade")
    is_last_stage = fields.Boolean(string="Is Last Stage",
        related="stage_id.is_last_stage")
    remaining_duration = fields.Float(string="Remaining Duration",
        compute="_compute_remaining_duration",
        store=True)
    target_duration = fields.Float(string="Target Duration",
        readonly=True)
    status = fields.Char(string="Running Status",
        compute="_compute_status")
    opportunity_date = fields.Datetime(string="Opportunity Date",
        related="lead_id.opportunity_date",
        store=True)
    final_status = fields.Char(string="Final Status",
        compute="_compute_final_status",
        store=True)
    final_actual_duration = fields.Float(string="Final Duration",
        compute="_compute_final_status",
        store=True)
    team_id = fields.Many2one(comodel_name="crm.team",
        string="Service",
        related="lead_id.team_id",
        store=True)
    partner_id = fields.Many2one(comodel_name="res.partner",
        string="Candidate",
        related="lead_id.partner_id",
        store=True)
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("start_date", "end_date")
    def _compute_actual_duration(self):
        for log in self:
            if log.end_date:
                duration = (log.end_date - log.start_date).total_seconds() / SECONDS_IN_A_DAY
            else:
                duration = (datetime.now() - log.start_date).total_seconds() / SECONDS_IN_A_DAY
            log.actual_duration = duration
            log.actual_duration_text = log.stage_id.duration_to_text(duration)

    def _compute_status(self):
        for log in self:
            if log.target_duration:
                remaining = log.remaining_duration - log.actual_duration
                if (remaining >= 0):
                    log.status = "Within"
                else:
                    log.status = "Beyond"
            else:
                log.status = "Within"
    
    @api.depends("lead_id.stage_log_ids", "target_duration")
    def _compute_remaining_duration(self):
        for log in self:
            previous_logs = self.search([("lead_id","=",log.lead_id.id),
                                         ("stage_id","=",log.stage_id.id),
                                         ("start_date","<",log.start_date),
                                         ("end_date","!=",False)])
            previous_duration = sum([l.actual_duration for l in previous_logs]) if previous_logs else 0.0
            log.remaining_duration = log.target_duration - previous_duration
    
    @api.depends("end_date")
    def _compute_final_status(self):
        for log in self:
            if log.end_date:
                log.final_actual_duration = log.actual_duration
                log.final_status = log.status
            else:
                log.final_actual_duration = 0
                log.final_status = False
        
    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################