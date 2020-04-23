# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api

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
    stage_log_ids = fields.One2many(string="Stage Logs",
        comodel_name="crm.lead.stage.log",
        inverse_name="lead_id")
    duration_in_stage = fields.Float(string="Duration in Stage",
        compute="_compute_duration")
    duration_in_stage_text = fields.Char(string="Duration in Stage",
        compute="_compute_duration")
    total_duration = fields.Float(string="Total Duration",
        compute="_compute_duration",
        help="Sum of all actual durations excluding those in last stage")
    total_duration_text = fields.Char(string="Total Duration",
        compute="_compute_duration")
    duration_status = fields.Selection(string="Duration Status",
        selection=[
            ("within", "Within Target"),
            ("beyond", "Beyond Target")],
        compute="_compute_duration",
        help="Within target if duration in stage is less than target or target is 0")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("stage_log_ids")
    def _compute_duration(self):
        for lead in self:
            # duration in stage
            lead.duration_in_stage = \
                sum(log.actual_duration for log in \
                    lead.stage_log_ids.filtered(lambda l: l.stage_id == lead.stage_id))
            lead.duration_in_stage_text = lead.stage_id.duration_to_text(lead.duration_in_stage)

            # duration status
            if lead.duration_in_stage <= lead.stage_id.target_duration or \
               lead.stage_id.target_duration == 0.0:
                lead.duration_status = "within"
            else:
                lead.duration_status = "beyond"

            # total duration
            lead.total_duration = \
                sum(log.actual_duration for log in \
                    lead.stage_log_ids.filtered(lambda l: l.stage_id.is_last_stage == False))
            lead.total_duration_text = lead.stage_id.duration_to_text(lead.total_duration)
    
    ############################
    # Constrains and onchanges #
    ############################
    @api.constrains("stage_id", "user_id")
    def _record_stage_log(self):
        current_time = datetime.now()
        for lead in self:
            if lead.type == "opportunity" and lead.stage_id.id:
                # end last log
                if lead.stage_log_ids:
                    last_log = lead.stage_log_ids[-1]
                    last_log.end_date = current_time

                # create new log
                log_obj = self.env["crm.lead.stage.log"]
                log_obj.create({
                    "lead_id": lead.id,
                    "stage_id": lead.stage_id.id,
                    "user_id": lead.user_id and lead.user_id.id,
                    "start_date": current_time,
                })

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################