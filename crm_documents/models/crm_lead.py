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
    major_document_ids = fields.One2many(string="Major Documents",
        comodel_name="crm.lead.document",
        inverse_name="lead_id")
    minor_document_ids = fields.One2many(string="Minor Documents",
        comodel_name="crm.lead.document",
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