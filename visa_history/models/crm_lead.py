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
        compute="_compute_visa_expiration_date",
        store=True,
        help="Gets the latest expiration date available")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("visa_ids", "visa_ids.expiration_date")
    def _compute_visa_expiration_date(self):
        for lead in self:
            result = False
            visa_ids = lead.visa_ids.filtered(lambda l: l.expiration_date)
            if visa_ids:
                result = visa_ids.sorted("expiration_date")[-1].expiration_date
            lead.visa_expiration_date = result

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