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
    visa_ids = fields.One2many(string="Visas",
        comodel_name="crm.lead.visa",
        inverse_name="lead_id")
    visa_expiration_date = fields.Date(string="Visa Expiration",
        compute="_compute_visa_details",
        store=True,
        help="Gets the expiration date of the newest visa")
    visa_type = fields.Selection(string="Visa Type",
        selection=[
            ("diploma", "Diploma"),
            ("leadership", "Leadership")],
        compute="_compute_visa_details",
        store=True)
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("visa_ids", "visa_ids.expiration_date", "visa_ids.type")
    def _compute_visa_details(self):
        for lead in self:
            lead.visa_type = False
            lead.visa_expiration_date = False
            visa_ids = lead.visa_ids.filtered(lambda l: l.start_date)
            if visa_ids:
                lead.visa_type = visa_ids[-1].type
                lead.visa_expiration_date = visa_ids[-1].expiration_date
            

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