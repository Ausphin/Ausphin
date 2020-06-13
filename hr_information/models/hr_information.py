# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    relation = fields.Char(string='Emergency Contact Information', help='Relation with employee')
    employee_obj = fields.Many2one('hr.employee', invisible=1)

    p_address = fields.Many2one('res.partner',string="Permanent Home Address")
    prsnl_contact_detail = fields.Char(string="personal Contact Detail")
    gov_id = fields.Integer(string="Goverment ID Numbers")


    h_date = fields.Date(string="Hiering Date")
    salary = fields.Float(string="Salary")
    tax_status = fields.Char(string="Tax Status")
    b_acc_no = fields.Integer(string="Bank Account Number")
    emp_aniversery = fields.Date(string="Employee Anniversary Date")
