# -*- coding: utf-8 -*-
import random
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
    stage_id = fields.Many2one(comodel_name="crm.stage",
        store=True,
        string="Stage")
    
    ##############################
    # Compute and search methods #
    ##############################        
        

    ############################
    # Constrains and onchanges #
    ############################

    @api.onchange("team_id")
    def _onchange_sales_team(self):
        self.user_id = False
    
        min = 999999999
        results = []
        
        stage = self.env["crm.stage"].sudo().search([("team_id","=",self.team_id.id)], limit=1).id
        stage_id = self.env["crm.stage"].browse(stage)
        self.stage_id = stage_id.id
        
                        
        for assignable_id in stage_id.assignable_ids:
            opportunity_count = self.env["crm.lead"].sudo().search_count([("stage_id","=",stage_id.id),("user_id","=",assignable_id.id)])
            if not opportunity_count:
                opportunity_count = 0
            
            if opportunity_count < min:
                min = opportunity_count
                results = [assignable_id.id]
            elif opportunity_count == min:
                results.append(assignable_id.id)
        
        if len(results) > 1:
            self.user_id = random.choice(results)
        
        elif len(results) == 1:
            self.user_id = results[0]
            
        
        
    #########################
    # CRUD method overrides #
    #########################
    
    
    ##################
    # Action methods #
    ##################
    @api.multi
    def action_apply(self):
        self.ensure_one()
        return super(Lead2OpportunityPartner, self.with_context(stage_id=self.stage_id.id)).action_apply()
    
    ####################
    # Business methods #
    ####################