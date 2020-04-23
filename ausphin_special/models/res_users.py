from odoo import models, fields, api

class ResUsers(models.Model):
    
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
    @api.model
    def create(self, vals):
        self.clear_caches()
        return super(ResUsers, self).create(vals)

    @api.multi
    def write(self, vals):
        self.clear_caches()
        return super(ResUsers, self).write(vals)

    @api.multi
    def unlink(self):
        self.clear_caches()
        return super(ResUsers, self).unlink()

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################