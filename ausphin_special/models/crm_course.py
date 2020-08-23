# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api


class CrmCourse(models.Model):
    ######################
    # Private attributes #
    ######################
    _name = "crm.course"
    _description = "List of Courses"
    
    ###################
    # Default methods #
    ###################
  
        
    ######################
    # Fields declaration #
    ######################
    name = fields.Char(string="Course")
    
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