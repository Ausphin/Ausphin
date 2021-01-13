#-*- coding:utf-8 -*-


from odoo import api, fields, models, _
from datetime import date, datetime, time
import math
from pytz import timezone

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    date_payment = fields.Date(string="Payment Date")
    # day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)

    @api.model
    def get_hrs(self):
        work_hours = 0.0
        for rec in self:
            for line in rec.worked_days_line_ids:
                if line.code == "WORK100":
                    work_hours = line.number_of_hours
        return work_hours

    @api.model
    def get_ytd_details(self,line):
        amount = 0.0
        if line.slip_id.contract_id:
            if line.slip_id.contract_id.ytd_date:
                ytd_date = line.slip_id.contract_id.ytd_date
                payslip_lins = self.env['hr.payslip.line'].search([('slip_id.date_from','>=',ytd_date),('slip_id.employee_id','=',line.slip_id.employee_id.id),
                    ('salary_rule_id','=',line.salary_rule_id.id),('slip_id.state','not in',['draft','cancel'])])
                for li in payslip_lins:
                    amount += li.total
        
        return amount
    @api.model
    def get_leave_details(self):
        contract = self.contract_id
        
        day_from = datetime.combine(fields.Date.from_string(self.date_from), time.min)
        day_to = datetime.combine(fields.Date.from_string(self.date_to), time.max)
        day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)        
        current_leave_struct = {}
        leaves = {}
        calendar = contract.resource_calendar_id
        tz = timezone(calendar.tz)
        for day, hours, leave in day_leave_intervals:
                holiday = leave[:1].holiday_id
                current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
                    'name': holiday.holiday_status_id.name or _('Global Leaves'),
                    'sequence': 5,
                    'code': holiday.holiday_status_id.name or 'GLOBAL',
                    'number_of_days': 0.0,
                    'number_of_hours': 0.0,
                    'contract_id': contract.id,
                })
                current_leave_struct['number_of_hours'] += hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.combine(day, time.min)),
                    tz.localize(datetime.combine(day, time.max)),
                    compute_leaves=False,
                )
                if work_hours:
                    current_leave_struct['number_of_days'] += hours / work_hours
                    current_leave_struct['balance'] = contract.employee_id.remaining_leaves
        if current_leave_struct:
            return [current_leave_struct]
        else:
            return []
        


    @api.model
    def get_total_earning(self):
        basic_amount = 0.0
        net_amount = 0.0
        for rec in self:
            for line in rec.line_ids:
                if line.code == "BASIC":
                    basic_amount = line.total
            for line in rec.line_ids:
                if line.category_id.code == "NET":
                    net_amount = line.total

        return basic_amount

    @api.model
    def get_total_net_earning(self):
        basic_amount = 0.0
        net_amount = 0.0
        for rec in self:
            for line in rec.line_ids:
                if line.code == "BASIC":
                    basic_amount = line.total
            for line in rec.line_ids:
                if line.category_id.code == "NET":
                    net_amount = line.total

        return net_amount
        


class HrPayrollPaygwScale(models.Model):
    _name = 'hr.payroll.paygw.table'
    _description = 'Australian PAYG Withholding Scale'

    @api.model
    def year_selection(self):
        year = 2019
        year_list = []
        while year != 2026: 
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    name = fields.Char('Name', size=128)
    year = fields.Selection([('2018-2019','2018-2019'),('2019-2020','2019-2020'),('2020-2021','2020-2021'),('2021-2022','2021-2022'),('2022-2023','2022-2023'),('2023-2024','2023-2024'),('2024-2025','2024-2025')],string='Year')
    line_ids = fields.One2many('hr.payroll.paygw.table.line', 'table_id', 'Lines')
    older_line_ids = fields.One2many('hr.payroll.paygw.older.table.line', 'table_id', 'Lines', copy=True)
    older = fields.Boolean(string='2019 Older Tax*?', default=False)

class HrPayrollPaygwTableLine(models.Model):
    _name = 'hr.payroll.paygw.table.line'
    _description = 'PAYG Line'
    
    table_id = fields.Many2one('hr.payroll.paygw.table', 'Table')
    income = fields.Float('$', digits=(16, 2), required=True)
    coeff_a = fields.Float('Coefficient (a)', digits=(16, 4))
    coeff_b = fields.Float('Coefficient (b)', digits=(16, 4))

class HrPayrollPaygwOlderTableLine(models.Model):
    _name = 'hr.payroll.paygw.older.table.line'
    _description = 'PAYG Older Line'
    
    table_id = fields.Many2one('hr.payroll.paygw.table', 'Table')
    income = fields.Float(string="Earning", digits=(16, 2), required=True)
    with_tax_free = fields.Float('With Tax Free', digits=(16, 4))
    no_tax_free = fields.Float('No Tax Free', digits=(16, 4))
    

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
        

    taxtable = fields.Many2one('hr.payroll.paygw.table','2020 Tax*')
    taxtable_older = fields.Many2one('hr.payroll.paygw.table','2019 Tax*')

    def get_value_details(self, contract, amount, payslip):
        date_time_obj = datetime.strptime(str(payslip), '%Y-%m-%d')
        contract = str(contract)
        contracta = contract.replace('hr.contract(','')
        contractb = contracta.replace(',)','')
        contractc = contractb
        contractd = int(contractc)
        contract_id = self.env['hr.contract'].search([('id','=',contractd)])
        paygresult = 0
        if date_time_obj.year <= 2020 and date_time_obj.month <= 10:
            amount = (contract_id.rate_per_day * amount)
            scales = self.taxtable_older
            tableline_id = self.env['hr.payroll.paygw.older.table.line'].search([('table_id','=',self.taxtable.id),('income','<=',amount)],limit=1,order='id desc')
            paygresult = tableline_id.with_tax_free
            result = paygresult
            
        else:
            amount = (contract_id.rate_per_day * amount / 2) 
            amount = int(amount)
            scales = self.taxtable
            amount += 0.99
            tableline_id = self.env['hr.payroll.paygw.table.line'].search([('table_id','=',self.taxtable.id),('income','<=',amount)],limit=1,order='id desc')
            paygresult = (amount * tableline_id.coeff_a) - tableline_id.coeff_b
            result = round(paygresult)*2
        return result

class HrEmployeeContract(models.Model):
    _inherit = 'hr.contract'
        
    annual_salary = fields.Float('Annual Salary')
    superannuation = fields.Float('Superannuation')
    annual_leave_day = fields.Float('Annual Leave (days)')
    sick_leave_day = fields.Float('Sick Leave/Carer Leave (days)')
    rate_per_day = fields.Float(string='Rate / hrs',digits=(16, 4))
    weeks_per_year = fields.Integer(string='Weeks',default=52)
    weekly_rate = fields.Float(string='Weekly Rate')
    weekly_hrs = fields.Integer(string='Number of Hrs on Week',default=40)
    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('fortnightly','Fortnightly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),

    ], string='Scheduled Pay', index=True, default='monthly',
    help="Defines the frequency of the wage payment.")
    ytd_date = fields.Date("YTD Date")




    @api.onchange('annual_salary','weeks_per_year')
    def onchange_annual_salary(self):
        for rec in self:
            rec.weekly_rate = (rec.annual_salary / rec.weeks_per_year)
            rec.rate_per_day = (rec.weekly_rate / rec.weekly_hrs)
