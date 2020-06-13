# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import fields, models, api
from odoo.tools.translate import _

class hr_company_holidays(models.Model):
    _inherit = 'hr.leave.allocation'
    

    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('company', 'Company Given'),
        ('department', 'By Department'),
        ('category', 'By Employee Tag'),
        ('government','Gov’t Mandated')],
        string='Allocation Mode', readonly=True, required=True, default='employee',
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        help="Allow to create requests in batchs:\n- By Employee: for a specific employee"
             "\n- Company Given: all employees of the specified company"
             "\n- By Department: all employees of the specified department"
             "\n- By Employee Tag: all employees of the specific employee group category"
             "\n- Gov’t Mandated: all employees of the specified government mandated")


    government_id = fields.Selection([
        ('maternity_leave', 'SSS Maternity Leave'), ('paternity_leave', 'SSS Paternity Leave'),('parent_leave','Solo Parent Leave'),('other_leave','Others (Magna Carta for Women)')],
        string="Gov’t Mandated Leave", default='paternity_leave')


    _sql_constraints = [
        ('type_value',
         "CHECK( (holiday_type='employee' AND employee_id IS NOT NULL) or "
         "(holiday_type='category' AND category_id IS NOT NULL) or "
         "(holiday_type='department' AND department_id IS NOT NULL) or "
         "(holiday_type='government' AND government_id IS NOT NULL) or "
         "(holiday_type='company' AND mode_company_id IS NOT NULL))",
         "The employee, department, company or employee category of this request is missing. Please make sure that your user login is linked to an employee."),
        ('duration_check', "CHECK ( number_of_days >= 0 )", "The number of days must be greater than 0."),
        ('number_per_interval_check', "CHECK(number_per_interval > 0)", "The number per interval should be greater than 0"),
        ('interval_number_check', "CHECK(interval_number > 0)", "The interval number should be greater than 0"),
    ]


    @api.onchange('holiday_type')
    def _onchange_type(self):
        if self.holiday_type == 'employee':
            if not self.employee_id:
                self.employee_id = self.env.user.employee_ids[:1].id
            self.mode_company_id = False
            self.category_id = False
        elif self.holiday_type == 'company':
            self.employee_id = False
            if not self.mode_company_id:
                self.mode_company_id = self.env.user.company_id.id
            self.category_id = False
        elif self.holiday_type == 'department':
            self.employee_id = False
            self.mode_company_id = False
            self.category_id = False
            if not self.department_id:
                self.department_id = self.env.user.employee_ids[:1].department_id.id
        elif self.holiday_type == 'category':
            self.employee_id = False
            self.mode_company_id = False
            self.department_id = False
        elif self.holiday_type == 'government':
            self.government_id = False



    @api.multi
    def name_get(self):
        res = []
        for allocation in self:
            if allocation.holiday_type == 'company':
                target = allocation.mode_company_id.name
            elif allocation.holiday_type == 'department':
                target = allocation.department_id.name
            elif allocation.holiday_type == 'category':
                target = allocation.category_id.name
            elif allocation.holiday_type == 'government':
                target = allocation.government_id
            else:
                target = allocation.employee_id.name

            res.append(
                (allocation.id,
                 _("Allocation of %s : %.2f %s to %s") %
                 (allocation.holiday_status_id.name,
                  allocation.number_of_hours_display if allocation.type_request_unit == 'hour' else allocation.number_of_days,
                  'hours' if allocation.type_request_unit == 'hour' else 'days',
                  target))
            )
        return res


    def _action_validate_create_childs(self):
        childs = self.env['hr.leave.allocation']
        if self.state == 'validate' and self.holiday_type in ['category', 'department', 'company','government']:
            if self.holiday_type == 'category':
                employees = self.category_id.employee_ids
            elif self.holiday_type == 'department':
                employees = self.department_id.member_ids
            else:
                employees = self.env['hr.employee'].search([('company_id', '=', self.mode_company_id.id)])

            for employee in employees:
                childs += self.with_context(
                    mail_notify_force_send=False,
                    mail_activity_automation_skip=True
                ).create(self._prepare_holiday_values(employee))
            # TODO is it necessary to interleave the calls?
            childs.action_approve()
            if childs and self.holiday_status_id.validation_type == 'both':
                childs.action_validate()
        return childs