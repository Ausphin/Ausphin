# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmTrainingVenue(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.training.venue"
    _description = "Training Venue"
    _order = "name"
    
    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Name",
        required=True)
    trainee_ids = fields.One2many(string="Trainees",
        comodel_name="crm.training",
        inverse_name="venue_id",
        domain=[('interview_result','=','successful'),('jo_acceptance_date','!=',False)])
    supervisor_ids = fields.Many2many(string="Accredited Supervisors",
        comodel_name="res.partner",
        relation="venue_partner_rel")
    
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