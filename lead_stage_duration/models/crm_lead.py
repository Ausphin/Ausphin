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
        compute="_compute_duration_in_stage")
    duration_status = fields.Selection(string="Duration Status",
        selection=[
            ("within", "Within Target"),
            ("beyond", "Beyond Target")],
        compute="_compute_duration_status")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("stage_log_ids")
    def _compute_duration_in_stage(self):
        for lead in self:
            lead.duration_in_stage = \
                sum(log.actual_duration for log in \
                    lead.stage_log_ids.filtered(lambda l: l.stage_id == lead.stage_id))
    
    @api.depends("duration_in_stage")
    def _compute_duration_status(self):
        for lead in self:
            if lead.duration_in_stage <= lead.stage_id.target_duration:
                lead.duration_status = "within"
            else:
                lead.duration_status = "beyond"
    
    ############################
    # Constrains and onchanges #
    ############################
    @api.constrains("stage_id", "user_id")
    def _record_stage_log(self):
        current_time = datetime.now()
        for lead in self:
            if lead.type == "opportunity":
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