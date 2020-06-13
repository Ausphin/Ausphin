# -*- coding: utf-8 -*-


from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    health_condition_ids = fields.One2many(
        string='Health Conditions',
        comodel_name='hr.employee.health.condition',
        inverse_name='employee_id',
        groups='hr.group_hr_user',
    )
    blood_type = fields.Many2one(
        string='Blood Type',
        comodel_name='hr.employee.blood.type',
        groups='hr.group_hr_user',
    )
    health_notes = fields.Text(
        string='Health Notes',
        groups='hr.group_hr_user',
    )


class HrEmployeeBloodType(models.Model):
    _name = 'hr.employee.blood.type'
    _description = 'HR Employee Blood Type'

    name = fields.Char(
        string='Type',
        required=True,
        translate=True
    )


class HrEmployeeHealthCondition(models.Model):
    _name = 'hr.employee.health.condition'
    _description = 'HR Employee Health Condition'

    employee_id = fields.Many2one(
        string='Employee',
        comodel_name='hr.employee',
    )
    type_id = fields.Many2one(
        'hr.employee.health.condition.type',
        string='Condition',
        required=True,
    )
    severity_id = fields.Many2one(
        'hr.employee.health.condition.severity',
        string='Severity',
    )
    notes = fields.Text(
        string='Notes',
    )

class HrEmployeeHealthConditionSeverity(models.Model):
    _name = 'hr.employee.health.condition.severity'
    _description = 'HR Employee Health Condition Severity'

    name = fields.Char(
        string='Severity',
        required=True,
        translate=True
    )


class HrEmployeeHealthConditionType(models.Model):
    _name = 'hr.employee.health.condition.type'
    _description = 'HR Employee Health Condition Type'

    name = fields.Char(
        string='Type',
        required=True,
        translate=True
    )