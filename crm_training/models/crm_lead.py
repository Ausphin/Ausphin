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
    training_ids = fields.One2many(string="Training",
        comodel_name="crm.training",
        inverse_name="lead_id")
    partner_placement_position = fields.Char(string="Placement Position",
        related="partner_id.placement_position")
    training_start_date = fields.Date(string="Training Start Date",
        compute="_compute_training_start_date",
        store=True)
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("training_ids.start_date")
    def _compute_training_start_date(self):
        for record in self:
            result = False
            trainings = record.training_ids.filtered(lambda r: r.start_date)
            if trainings:
                result = trainings.sorted(key='start_date')[-1].start_date
            record.training_start_date = result
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