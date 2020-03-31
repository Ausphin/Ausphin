# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLeadVisa(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.lead.visa"
    _description = "Visa details for an opportunity"
    _order = "start_date, id"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Visa No.",
        required=True)
    lead_id = fields.Many2one(string="Lead/Opportunity",
        comodel_name="crm.lead",
        required=True)
    type = fields.Selection(string="Type",
        selection=[
            ("diploma", "Diploma"),
            ("leadership", "Leadership")])
    start_date = fields.Date(string="Start Date")
    expiration_date = fields.Date(string="Expiration Date")
    
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