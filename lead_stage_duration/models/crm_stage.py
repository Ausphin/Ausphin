# -*- coding: utf-8 -*-

from math import floor, ceil

from odoo import models, fields, api

HOURS_IN_A_DAY = 24

class CrmStage(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.stage"
    
    ###################
    # Default methods #
    ###################
    def name_get(self):
        result = []
        for stage in self:
            name = stage.name + " (" + str(stage.average_duration_text) + ")"
            result.append((stage.id, name))
        return result

    ######################
    # Fields declaration #
    ######################
    target_duration = fields.Float(string="Target Duration (Days)")
    target_duration_text = fields.Char(string="Target Duration",
        compute="_compute_target_duration_text")
    average_duration = fields.Float(string="Average Duration (Days)",
        compute="_compute_average_duration")
    average_duration_text = fields.Char(string="Average Duration",
        compute="_compute_average_duration")
    is_last_stage = fields.Boolean(string="Is Last Stage",
        compute="_compute_is_last_stage")
    current_within = fields.Integer(string="Current Within Target",
        compute="_compute_stats")
    current_beyond = fields.Integer(string="Current Beyond Target",
        compute="_compute_stats")
    total_within = fields.Integer(string="Total Within Target",
        compute="_compute_stats")
    total_beyond = fields.Integer(string="Total Beyond Target",
        compute="_compute_stats")
    lead_ids = fields.One2many(string="Leads",
        comodel_name="crm.lead",
        inverse_name="stage_id")
    log_ids = fields.One2many(string="Logs",
        comodel_name="crm.lead.stage.log",
        inverse_name="stage_id")
    ##############################
    # Compute and search methods #
    ##############################
    @api.multi
    @api.depends("target_duration")
    def _compute_target_duration_text(self):
        for stage in self:
            stage.target_duration_text = self.duration_to_text(stage.target_duration)
    
    @api.multi
    def _compute_average_duration(self):
        for stage in self:
            log_obj = self.env["crm.lead.stage.log"]
            leads = self.env["crm.lead"].search([('stage_id', '=', stage.id)])
            result = 0.0
            if leads:
                total = sum(l.duration_in_stage for l in leads)
                result = total / len(leads)
            stage.average_duration = result
            stage.average_duration_text = self.duration_to_text(result)

    @api.depends("team_id")
    def _compute_is_last_stage(self):
        for stage in self:
            result = False
            stage_ids = stage.sudo().search([("team_id","=",stage.team_id.id)]).ids
            current_stage_index = stage_ids.index(stage.id)
            if current_stage_index == (len(stage_ids) - 1):
                result = True
            stage.is_last_stage = result
    
    @api.multi
    def _compute_stats(self):
        for stage in self:
            current_within = 0
            current_beyond = 0
            for lead in stage.lead_ids:
                if lead.duration_status == 'within':
                    current_within += 1
                else:
                    current_beyond += 1
            
            stage.current_within = current_within
            stage.current_beyond = current_beyond
            within = set()
            beyond = set()
            for log in stage.log_ids:
                if log.status == 'Within':
                    within.add(log.lead_id.id)
                else:
                    beyond.add(log.lead_id.id)
                
            new_set = within - beyond
            
            stage.total_within = len(new_set)
            stage.total_beyond = len(beyond)
            
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
    def duration_to_text(self, duration):
        days = int(floor(duration))
        hours = int(ceil((duration % 1) * HOURS_IN_A_DAY))
        text = ""
        if days:
            text = "{}D".format(days)
        text += "{}H".format(hours)
        return text