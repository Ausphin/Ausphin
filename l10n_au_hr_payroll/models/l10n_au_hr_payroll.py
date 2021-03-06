#-*- coding:utf-8 -*-


from odoo import api, fields, models, _
from datetime import date, datetime, time
import math
from pytz import timezone

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    
    date_payment = fields.Date(string="Payment Date")
    working_days_count = fields.Float("Working Days Count", compute="get_total_working_hrs")
    working_hrs_count = fields.Float("Working Hrs Count", compute="get_total_working_hrs")
    
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
        amount_final = 0.0
        if line.slip_id.contract_id:
            if line.slip_id.contract_id.ytd_date:
                ytd_date = line.slip_id.contract_id.ytd_date
                payslip_lins = self.env['hr.payslip.line'].search([('slip_id.date_from','>=',ytd_date),('slip_id.employee_id','=',line.slip_id.employee_id.id),
                    ('salary_rule_id','=',line.salary_rule_id.id),('slip_id.state','not in',['draft','cancel']),
                    ('slip_id.date_from','<=',line.slip_id.date_from)])
                for li in payslip_lins:
                    amount += li.total
        amount_final = float(format(amount, '.2f'))
        return amount_final

    @api.model
    def get_leave_details(self):
        contract = self.contract_id
        day_from = datetime.combine(fields.Date.from_string(self.date_from), time.min)
        day_to = datetime.combine(fields.Date.from_string(self.date_to), time.max)
        
        from_date = str(day_to.year)+ "-01-01"
        end_date = str(day_to.year)+ "-12-31"

        # used sick leave
        used_sick_leave = self.env['hr.leave'].search([('holiday_status_id.sick_leav','=',True),
            ('date_from','>=',from_date),
            # ('date_to','<=',self.date_to),
            ('employee_id','=',self.employee_id.id)
            ])
        used_sick_leave_count = 0
        for sick in used_sick_leave:
            if sick.date_to.month <= self.date_to.month:
                used_sick_leave_count += sick.number_of_days_display

        # use_annual_leave
        used_annual_leave = self.env['hr.leave'].search([('holiday_status_id.annual_leav','=',True),
            ('date_from','>=',from_date),
            # ('date_to','<=',self.date_to),
            ('employee_id','=',self.employee_id.id)
            ])
        used_annual_leave_count = 0
        for sick in used_annual_leave:
            if sick.date_to.month <= self.date_to.month:
                used_annual_leave_count += sick.number_of_days_display

        # allocated sick leave
        leave_Allocated = self.env['hr.leave.allocation'].search([('holiday_status_id.sick_leav','=',True),
            ('holiday_status_id.validity_start','>=',from_date),
            ('holiday_status_id.validity_stop','<=',end_date),
            ('employee_id','=',self.employee_id.id)
            ])
        leave_details = []
        allocate_leave_count = 0
        for sick in leave_Allocated:
            if sick.accrual:
                allocate_leave_count += sick.number_of_days_display
            elif sick.date_to.month <= day_to.month and sick.date_to.year == day_to.year:
                allocate_leave_count += sick.number_of_days_display

        leave_details.append({'Name':'Sick Leave','totol_balance':allocate_leave_count-used_sick_leave_count,'totol_used':used_sick_leave_count})

        # annual leave
        annual_leave_Allocated = self.env['hr.leave.allocation'].search([('holiday_status_id.annual_leav','=',True),
            ('holiday_status_id.validity_start','>=',from_date),
            ('holiday_status_id.validity_stop','<=',end_date),
            ('employee_id','=',self.employee_id.id)
            ])
        annual_allocate_leave_count = 0
        for sick in annual_leave_Allocated:
            if sick.accrual:
                annual_allocate_leave_count += sick.number_of_days_display
            elif sick.date_to.month <= day_to.month and sick.date_to.year == day_to.year:
                annual_allocate_leave_count += sick.number_of_days_display
            
            
        leave_details.append({'Name':'Annual Leave','totol_balance':annual_allocate_leave_count-used_annual_leave_count,'totol_used':used_annual_leave_count})


        return leave_details

        # day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)        
        
        # day_from = datetime.combine(fields.Date.from_string(self.date_from), time.min)
        # day_to = datetime.combine(fields.Date.from_string(self.date_to), time.max)
        # day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)        
        # current_leave_struct = {}
        # leaves = {}
        # calendar = contract.resource_calendar_id
        # tz = timezone(calendar.tz)
        # for day, hours, leave in day_leave_intervals:
        #         holiday = leave[:1].holiday_id
        #         current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
        #             'name': holiday.holiday_status_id.name or _('Global Leaves'),
        #             'sequence': 5,
        #             'code': holiday.holiday_status_id.name or 'GLOBAL',
        #             'number_of_days': 0.0,
        #             'number_of_hours': 0.0,
        #             'contract_id': contract.id,
        #         })
        #         current_leave_struct['number_of_hours'] += hours
        #         work_hours = calendar.get_work_hours_count(
        #             tz.localize(datetime.combine(day, time.min)),
        #             tz.localize(datetime.combine(day, time.max)),
        #             compute_leaves=False,
        #         )
        #         if work_hours:
        #             current_leave_struct['number_of_days'] += hours / work_hours
        #             current_leave_struct['balance'] = contract.employee_id.remaining_leaves
        # if current_leave_struct:
        #     return [current_leave_struct]
        # else:
        #     return []
        


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

        basic_amount_final = float(format(basic_amount, '.2f'))
        return basic_amount_final

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

        net_amount_final = float(format(net_amount, '.2f'))
        return net_amount_final


    def get_total_working_hrs(self):
        days = 0.0
        hours = 0.0
        for line in self.worked_days_line_ids:
            if line.code == "WORK100":
                days += line.number_of_days
                hours += line.number_of_hours
            else:
                if "Sick" in line.code or "Sick" in line.name or "SL" in line.code:
                    days += line.number_of_days
                    hours += line.number_of_hours
                if "Annual" in line.code or "Annual" in line.name or "AL" in line.code:
                    days += line.number_of_days
                    hours += line.number_of_hours
        self.working_days_count = days
        self.working_hrs_count = hours
        
        


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

    def get_value_details(self, contract, amount, payslip, dateto):
        date_time_obj = datetime.strptime(str(payslip), '%Y-%m-%d')
        date_timeto_obj = datetime.strptime(str(dateto), '%Y-%m-%d')

        contract = str(contract)
        contracta = contract.replace('hr.contract(','')
        contractb = contracta.replace(',)','')
        contractc = contractb
        contractd = int(contractc)
        contract_id = self.env['hr.contract'].search([('id','=',contractd)])
        paygresult = 0
        if date_time_obj.year <= 2020:
            if date_time_obj.year == 2020 and date_time_obj.month == 10 and date_time_obj.day <= 13:
                if date_time_obj.day < 13 and date_timeto_obj.day < 13:
                    amount = (contract_id.rate_per_day * amount)
                    scales = self.taxtable_older
                    tableline_id = self.env['hr.payroll.paygw.older.table.line'].search([('table_id','=',self.taxtable_older.id),('income','<=',amount)],limit=1,order='id desc')
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
            else:
                if date_time_obj.year >= 2020 and date_time_obj.month >= 10:
                    amount = (contract_id.rate_per_day * amount / 2) 
                    amount = int(amount)
                    scales = self.taxtable
                    amount += 0.99
                    tableline_id = self.env['hr.payroll.paygw.table.line'].search([('table_id','=',self.taxtable.id),('income','<=',amount)],limit=1,order='id desc')
                    paygresult = (amount * tableline_id.coeff_a) - tableline_id.coeff_b
                    result = round(paygresult)*2
                else:
                    amount = (contract_id.rate_per_day * amount)
                    scales = self.taxtable_older
                    tableline_id = self.env['hr.payroll.paygw.older.table.line'].search([('table_id','=',self.taxtable_older.id),('income','<=',amount)],limit=1,order='id desc')
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

