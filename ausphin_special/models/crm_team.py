from odoo import models, fields, api, exceptions

class CrmTeam(models.Model):
    
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
        return super(CrmTeam, self).create(vals)

    @api.multi
    def write(self, vals):
        self.clear_caches()
        return super(CrmTeam, self).write(vals)

    @api.multi
    def unlink(self):
        self.clear_caches()
        return super(CrmTeam, self).unlink()

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################