# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _
from odoo.http import request


class EmployeeReminder(models.Model):
    _inherit = "hr.employee"


    @api.model
    def birthday_mail_method(self):
        ctx = self._context.copy()
        template_id = self.env.ref(
            "hr_information.email_template_employee_birthday_notification")
        current_date = date.today()
        for employee in self.search([]):
            if employee.birthday:
                current_date = date.today()
                employee_birthday = datetime.strptime(
                    str(employee.birthday), "%Y-%m-%d")
                full_year_passed = (current_date.month, current_date.day) == (
                    employee_birthday.month, employee_birthday.day)
                if full_year_passed:
                    ctx.update({'body_action': employee.user_id.body_action or
                                self.env.user.company_id.body_action,
                                'report_header': employee.user_id.report_header or
                                self.env.user.company_id.report_header,
                                'report_footer': employee.user_id.report_footer or
                                self.env.user.company_id.report_footer})
                    template_id.with_context(ctx).send_mail(employee.id)


    @api.model
    def aniversary_mail_method(self):
        ctx = self._context.copy()
        template_id = self.env.ref(
            "hr_information.email_template_employee_aniversary_notification")
        current_date = date.today()
        for employee in self.search([]):
            if employee.emp_aniversery:
                current_date = date.today()
                employee_aniversery = datetime.strptime(
                    str(employee.emp_aniversery), "%Y-%m-%d")
                full_year_passed = (current_date.month, current_date.day) == (
                    employee_aniversery.month, employee_aniversery.day)
                if full_year_passed:
                    ctx.update({'ani_body': employee.user_id.ani_body or
                                self.env.user.company_id.ani_body,
                                'ani_header': employee.user_id.ani_header or
                                self.env.user.company_id.ani_header,
                                'ani_footer': employee.user_id.ani_footer or
                                self.env.user.company_id.ani_footer})
                    template_id.with_context(ctx).send_mail(employee.id)
                    