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
    show_in_conversion = fields.Boolean(string="Show in Lead Conversion")
    
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