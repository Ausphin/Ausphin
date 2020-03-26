# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Lead2OpportunityPartner(models.TransientModel):
        
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.lead2opportunity.partner"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    
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