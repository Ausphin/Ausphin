# -*- coding: utf-8 -*-

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