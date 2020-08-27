# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api


class CrmVisaType(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.visa.type"
    _description = "List of Visa Types"
    
    ###################
    # Default methods #
    ###################
  
        
    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Visa Type")
    
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