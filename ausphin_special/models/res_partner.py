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
    active_opportunity_count = fields.Integer("Active Opportunity",
        compute="_compute_active_opportunity_count")
    has_active_opportunity = fields.Boolean(string="Has Active Opportunity",
        compute="_compute_active_opportunity_count",
        search="_search_has_active_opportunity")
    citizenship_id = fields.Many2one(string="Citizenship",
        comodel_name="res.country")
    venue_ids = fields.Many2many(string="Training Venues",
        comodel_name="crm.training.venue",
        relation="venue_partner_rel")
    gender = fields.Selection(string="Gender",
        selection=[
            ("male","Male"),
            ("female","Female")])

    
    ##############################
    # Compute and search methods #
    ##############################
    @api.multi
    def _compute_active_opportunity_count(self):
        for partner in self:
            operator = 'child_of' if partner.is_company else '='  # the opportunity count should counts the opportunities of this company and all its contacts
            leads = self.env['crm.lead'].search([('partner_id', operator, partner.id), ('type', '=', 'opportunity')])
            active_leads = leads.filtered(lambda l: l.stage_id.is_last_stage == False)
            partner.active_opportunity_count = len(active_leads)
            partner.has_active_opportunity = active_leads and True or False
    
    def _search_has_active_opportunity(self, operator, value):
        ids = self.search([]).filtered(lambda l: l.has_active_opportunity == True).ids
        domain_operator = "in" if operator == "=" else "not in"
        return [("id", domain_operator, ids)]

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