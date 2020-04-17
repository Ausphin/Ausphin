from odoo import models, fields, api

class ResPartner(models.Model):
    
    ######################
    # Private attributes #
    ######################
    _inherit = "res.partner"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    civil_status = fields.Selection(string="Civil Status",
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("widowed", "Widowed"),
            ("divorced","Divorced")])
    religion = fields.Char(string="Religion")
    birth_place = fields.Char(string="Place of Birth")
    birth_date = fields.Date(string="Date of Birth")
    
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