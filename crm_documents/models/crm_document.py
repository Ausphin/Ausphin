# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmDocument(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.document"
    _description = "CRM Document"
    
    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Name",
        required=True)
    type = fields.Selection(string="Type",
        required=True,
        selection=[
            ("major", "Major"),
            ("minor", "Minor"),
            ("scholar", "Scholar")])
    
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