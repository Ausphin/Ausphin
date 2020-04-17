# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "sale.order"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    total_paid = fields.Float(string="Total Paid",
        compute="_compute_total_paid")
    
    ##############################
    # Compute and search methods #
    ##############################
    def _compute_total_paid(self):
        for order in self:
            result = 0
            total_amount = 0
            total_residual = 0

            for invoice in order.invoice_ids:
                if invoice.state == "open":
                    total_amount += invoice.amount_total
                    total_residual += invoice.residual

            if total_amount:    
                result = (total_amount - total_residual)

            order.total_paid = result

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