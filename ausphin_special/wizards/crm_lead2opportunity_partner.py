# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Lead2OpportunityPartner(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"