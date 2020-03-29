# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmTraining(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.training"
    _description = "Training"
    
    ###################
    # Default methods #
    ###################
    def name_get(self):
        result = []
        for training in self:
            name = training.venue_id.name + " - " + \
                   (training.lead_id.partner_id.name or "Lead #" + str(training.lead_id.id))
            result.append((training.id, name))
        return result

    ######################
    # Fields declaration #
    ######################
    lead_id = fields.Many2one(string="Trainee",
        comodel_name="crm.lead",
        required=True)
    venue_id = fields.Many2one(string="Venue",
        comodel_name="crm.training.venue",
        required=True)
    endorsement_date = fields.Date(string="Endorsement Date")
    interview_date = fields.Date(string="Interview Date")
    interview_result = fields.Selection(string="Interview Result",
        selection=[
            ("pass", "Pass"),
            ("fail", "Fail")])
    job_offer_date = fields.Date(string="Job Offer Date")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    
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