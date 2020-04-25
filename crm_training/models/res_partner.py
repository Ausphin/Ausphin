# -*- coding: utf-8 -*-

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
    placement_position = fields.Char(string="Placement Position",
        compute="_compute_placement_position",
        store=True)
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("opportunity_ids.training_ids",
                 "opportunity_ids.training_ids.interview_result",
                 "opportunity_ids.training_ids.jo_acceptance_date")
    def _compute_placement_position(self):
        for partner in self:
            result = False
            trainings = self.env["crm.training"].sudo().search(
                [("partner_id","=",partner.id),("interview_result","=","successful"),("jo_acceptance_date","!=",False)])
            if trainings:
                result = trainings.sorted(key=lambda t: t.jo_acceptance_date)[-1].position
            else:
                trainings = self.env["crm.training"].sudo().search(
                    [("partner_id","=",partner.id),("interview_result","=","successful"),("jo_acceptance_date","=",False)])
                if trainings:
                    result = trainings[-1].position

            partner.placement_position = result
    
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