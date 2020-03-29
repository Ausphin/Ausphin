from odoo import models, fields, api, exceptions

class Users(models.Model):
    
    ######################
    # Private attributes #
    ######################
    _inherit = "res.users"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    stage_ids = fields.Many2many(comodel_name="crm.stage",
        relation="users_stages_rel",
        string="Assignable Stages")
    
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