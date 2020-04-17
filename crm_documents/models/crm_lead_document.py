# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLeadDocument(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.lead.document"
    _description = "Lead Document"
    
    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    document_id = fields.Many2one(string="Document",
        comodel_name="crm.document",
        required=True,
        ondelete="restrict")
    lead_id = fields.Many2one(string="Lead/Opportunity",
        comodel_name="crm.lead",
        required=True,
        ondelete="restrict")
    audit_date = fields.Date(string="Audit Date")
    expiry_date = fields.Date(string="Expiry Date")
    submit_date = fields.Date(string="Date Submitted")
    datas = fields.Binary(string="File")
    datas_fname = fields.Char("Filename")
    notarized = fields.Boolean(string="Notarized")
    remarks = fields.Text(string="Remarks")
    type = fields.Selection(string="Type",
        related="document_id.type",
        store=True)
    auditor = fields.Char(string="Auditor")
    interview_date = fields.Date(string="Interview Date")
    user_id = fields.Many2one(string="Responsible",
        comodel_name="res.users")
    result = fields.Float(string="Result (%)")
    
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