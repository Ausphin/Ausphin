from odoo import models, fields, api, exceptions

class Stages(models.Model):
    
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.stage"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    team_id = fields.Many2one(string="Journey",
        comodel_name="crm.team")
    assignable_ids = fields.Many2many(comodel_name="res.users",
        relation="users_stages_rel",
        string="Assignable Users",
        domain="[('sale_team_id','=',team_id)]")
    force_assign = fields.Boolean(string="Force Assign")
    
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