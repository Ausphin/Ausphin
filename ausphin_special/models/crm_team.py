from odoo import models, fields, api, exceptions

class Journey(models.Model):
    
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.team"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Journey")
    show_in_conversion = fields.Boolean(string="Show in Lead Conversion")
    is_with_site = fields.Boolean(string="Show Sites")
    
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