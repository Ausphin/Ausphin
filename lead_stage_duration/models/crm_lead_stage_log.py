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
    actual_duration = fields.Float(string="Actual Duration",
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