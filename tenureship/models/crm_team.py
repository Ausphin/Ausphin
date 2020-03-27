# -*- coding: utf-8 -*-

from odoo import fields, models, api

class CrmTeam(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.team"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    tenureship_basis_id = fields.Many2one(string="Tenureship Basis",
        comodel_name="ir.model.fields")
    
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