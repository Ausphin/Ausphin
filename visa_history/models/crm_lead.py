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
    visa_start_date = fields.Date(string="Visa Start Date",
        compute="_compute_visa_details",
        store=True,
        help="Gets the start date of the newest visa")
    visa_expiration_date = fields.Date(string="Visa Expiration",
        compute="_compute_visa_details",
        store=True,
        help="Gets the expiration date of the newest visa")
#     visa_type = fields.Selection(string="Visa Type",
#         selection=[
#             ("diploma", "Diploma"),
#             ("leadership", "Leadership"),
#             ("working", "Work"),
#             ("402", "402"),
#             ("407", "407"),
#             ("485", "485")],
#         compute="_compute_visa_details",
#         store=True)
    visa_type_id = fields.Many2one(string="Visa Type",
        comodel_name="crm.visa.type",
        compute="_compute_visa_details",
        store=True)
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("visa_ids", "visa_ids.expiration_date","visa_ids.start_date", "visa_ids.type_id")
    def _compute_visa_details(self):
        for lead in self:
            lead.visa_type_id = False
            lead.visa_start_date = False
            lead.visa_expiration_date = False
            visa_ids = lead.visa_ids.filtered(lambda l: l.start_date)
            if visa_ids:
                newest_visa = visa_ids.sorted(key="start_date")[-1]
                lead.visa_type_id = newest_visa.type_id.id
                lead.visa_start_date = newest_visa.start_date
                lead.visa_expiration_date = newest_visa.expiration_date

            

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