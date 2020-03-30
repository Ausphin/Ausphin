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
            name = stage.name + ' (' + str(stage.target_duration) + ')'
            result.append((stage.id, name))
        return result

    ######################
    # Fields declaration #
    ######################
    target_duration = fields.Float(string="Target Duration (Days)")
    
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

    ####################
    # Business methods #
    ####################