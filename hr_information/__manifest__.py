# -*- coding: utf-8 -*-
{
    'name': "HR Information",

    'summary': """Employee Document , Information""",

    'description': """Employee Document , Information""",

    'author': "Spellbound Soft Solutions",
    'website': "http://www.spellboundss.com",

    'category': 'hr',
    'version': '1.1',

    'depends': ['base','hr','hr_holidays','calendar'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_information.xml',
        'data/reminder.xml',
        'data/data.xml',
        'views/employee_helth.xml',
        'data/employee_helth_condition.xml',
        'views/res_company_view.xml',
        'views/res_users_view.xml',
        'views/hr_company_holidays_view.xml',
        'views/employee_document_view.xml',
    ],
}