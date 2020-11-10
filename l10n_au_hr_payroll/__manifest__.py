# -*- encoding: utf-8 -*-

{
	'name': 'Australian - Payroll',

    'description': """
            Australian Payroll Rules.
                """,

    'author': "Spellbound Soft Solutions",
    'website': 'http://www.spellboundss.com', 

    'category': 'Localization',
    'version': '0.3',

    'depends': ['hr_payroll','sale'],

    'data':[
        'data/l10n_au_hr_payroll_data.xml',
        'views/l10n_au_hr_payroll_view.xml',
		'security/ir.model.access.csv',
        'report/payslip_report_view.xml',
        'report/payslip_report_templates.xml',
    ],
 }
