# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "res.users"
    
    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    site_ids = fields.Many2many(comodel_name="crm.site",
        relation="users_sites_rel",
        string="Assignable Sites")
    
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
