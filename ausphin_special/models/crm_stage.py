# -*- coding: utf-8 -*-

import random

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
    company_id = fields.Many2one(string="Company",
        comodel_name="res.company",
        related="team_id.company_id")
    
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
    def get_assignee(self):
        min = 999999999
        result = False
        results = []

        for assignable_id in self.assignable_ids:
            opportunity_count = self.env["crm.lead"].sudo().\
                                search_count([("stage_id","=",self.id),("user_id","=",assignable_id.id)])
            if not opportunity_count:
                opportunity_count = 0
            
            if opportunity_count < min:
                min = opportunity_count
                results = [assignable_id.id]
            elif opportunity_count == min:
                results.append(assignable_id.id)
        
        if len(results) > 1:
            result = random.choice(results)
        elif len(results) == 1:
            result = results[0]

        return result