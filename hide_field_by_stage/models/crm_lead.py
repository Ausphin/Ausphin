# -*- coding: utf-8 -*-

import json
from lxml import etree

from odoo import models, fields, api

class CrmLead(models.Model):
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.lead"

    ###################
    # Default methods #
    ###################
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(CrmLead, self).fields_view_get(view_id, view_type, toolbar=toolbar,submenu=False)
        if view_type == "form":
            doc = etree.XML(res["arch"])
            nodes = doc.xpath("//*[@visibility]")
            for node in nodes:
                visibility = json.loads(node.get("visibility").replace("'", "\""))
                modifiers = {}
                if node.get("modifiers"):
                    modifiers = json.loads(node.get("modifiers"))

                to_add = []
                for key, value in visibility.items():
                    if self.env.user.has_group("sales_team.group_sale_salesman_all_leads") and key == "stage_id":
                        continue
                    to_add.append((key, "not in", value))

                if len(to_add) > 1:
                    # TODO: handling if there are more than 2 items to add
                    to_add = ['|'] + to_add

                if to_add:
                    if "invisible" in modifiers and isinstance(modifiers["invisible"], list):
                        # TODO: handling if there are more than 1 item in domain
                        modifiers["invisible"] = ['|'] + modifiers["invisible"]
                    else:
                        modifiers["invisible"] = []
                    modifiers["invisible"].extend(to_add)

                    node.set("modifiers", json.dumps(modifiers))
            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res

    ######################
    # Fields declaration #
    ######################
    
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
