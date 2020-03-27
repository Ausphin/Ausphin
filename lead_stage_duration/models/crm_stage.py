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

    ######################
    # Fields declaration #
    ######################
    target_duration = fields.Float(string="Target Duration")
    
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