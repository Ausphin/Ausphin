# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Lead2OpportunityPartner(models.TransientModel):
        
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.lead2opportunity.partner"

    ###################
    # Default methods #
    ###################
    
            
    ######################
    # Fields declaration #
    ######################
    team_id = fields.Many2one(string="Journey",
        comodel_name="crm.team")
    stage_id = fields.Many2one(comodel_name="crm.stage",
        store=True,
        string="Stage")
    site_id = fields.Many2one(string="Site",
        comodel_name="crm.site")
    is_with_site = fields.Boolean(related="team_id.is_with_site")
    
    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################
    @api.onchange("team_id")
    def _onchange_sales_team(self):
        stage_id = self.env["crm.stage"].sudo().search([("team_id","=",self.team_id.id)], limit=1).id
        stage = self.env["crm.stage"].sudo().browse(stage_id)
        self.stage_id = stage_id
        self.user_id = stage.sudo().get_assignee()
        self.site_id = False
 
    #########################
    # CRUD method overrides #
    #########################
    
    ##################
    # Action methods #
    ##################
    @api.multi
    def action_apply(self):
        self.ensure_one()
        super(Lead2OpportunityPartner, self.sudo().with_context(stage_id=self.stage_id.id,site_id=self.site_id.id)).action_apply()
        return self.env.ref("crm.crm_lead_all_leads").read()[0]
    
    ####################
    # Business methods #
    ####################