# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmSite(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.site"
    _description = "Lead/Opportunity Site"
    _order = "name"
    
    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Name",
        required=True)
    
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