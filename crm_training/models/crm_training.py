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
    lead_id = fields.Many2one(string="Lead/Opportunity",
        comodel_name="crm.lead",
        required=True)
    partner_id = fields.Many2one(string="Trainee",
        comodel_name="res.partner",
        related="lead_id.partner_id",
        store=True)
    venue_id = fields.Many2one(string="Venue",
        comodel_name="crm.training.venue",
        required=True)
    endorsement_date = fields.Date(string="Endorsement Date")
    interview_date = fields.Datetime(string="Interview Date")
    interview_result = fields.Selection(string="Interview Result",
        selection=[
            ("successful", "Successful"),
            ("not_yet_successful", "Not yet successful")])
    job_offer_date = fields.Date(string="Job Offer Date")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    supervisor_id = fields.Many2one(string="Workplace Supervisor",
        comodel_name="res.partner",
        domain="[('venue_ids','in',[venue_id])]")
    nominated_position = fields.Char(string="Nominated Position")
    position = fields.Char(string="Job Offer Position")
    jo_transmittal_date = fields.Date(string="JO Transmittal Date")
    jo_acceptance_date = fields.Date(string="JO Signed Date")
    annual_salary = fields.Float(string="Annual Salary (AUD)")
    remarks = fields.Text(string="Remarks")

    ##############################
    # Compute and search methods #
    ##############################
    
    ############################
    # Constrains and onchanges #
    ############################
    @api.onchange("venue_id")
    def _onchange_venue_id(self):
        self.supervisor_id = False

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################