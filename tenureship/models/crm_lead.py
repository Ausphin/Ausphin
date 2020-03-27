# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import floor

from odoo import fields, models, api

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
    tenureship = fields.Selection(string="Tenureship",
        selection=[
            ("0", "0"),
            ("3", "3"),
            ("6", "6"),
            ("9", "9"),
            ("12", "12")],
        compute="_compute_tenureship")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("team_id", "team_id.tenureship_basis_id")
    def _compute_tenureship(self):
        for lead in self:
            lead.tenureship = False
            basis = lead.team_id.tenureship_basis_id
            if basis:
                date = lead[basis.name]
                if date:
                    if isinstance(date, datetime):
                        date = date.date()
                    delta = relativedelta(datetime.today().date(), date)
                    diff = delta.years * 12 + delta.months
                    if diff < 0: diff = 0
                    lead.tenureship = str(12 if diff >= 12 else floor(diff / 3) * 3)

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