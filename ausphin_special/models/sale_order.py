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
    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                "partner_invoice_id": False,
                "partner_shipping_id": False,
                "payment_term_id": False,
                "fiscal_position_id": False,
            })
            return

        addr = self.partner_id.address_get(["delivery", "invoice"])
        values = {
            "pricelist_id": self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            "payment_term_id": self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            "partner_invoice_id": addr["invoice"],
            "partner_shipping_id": addr["delivery"],
        }
        if self.env["ir.config_parameter"].sudo().get_param("sale.use_sale_note") and self.env.user.company_id.sale_note:
            values["note"] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

        if self.partner_id.team_id:
            values["team_id"] = self.partner_id.team_id.id
        self.update(values)

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################