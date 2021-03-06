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
    assignable_ids = fields.Many2many(comodel_name="res.users",
        relation="users_sites_rel",
        string="Assignable Users")
    
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
