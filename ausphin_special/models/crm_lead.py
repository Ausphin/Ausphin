from odoo import models, fields, api, exceptions

class Lead(models.Model):
    
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
    team_id = fields.Many2one(comodel_name="crm.team",
        string="Journey",
        related="stage_id.team_id",
        store=True)
    
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