# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
            name = stage.name + ' (' + str(round(stage.average_duration, 2)) + ')'
            result.append((stage.id, name))
        return result

    ######################
    # Fields declaration #
    ######################
    target_duration = fields.Float(string="Target Duration (Days)")
    average_duration = fields.Float(string="Average Duration (Days)",
        compute="_compute_average_duration")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.multi
    def _compute_average_duration(self):
        for stage in self:
            leads = self.env["crm.lead"].search([('stage_id', '=', stage.id)])
            result = 0.0
            if leads:
                total = sum(l.duration_in_stage for l in leads)
                result = total / len(leads)
            stage.average_duration = result
    
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