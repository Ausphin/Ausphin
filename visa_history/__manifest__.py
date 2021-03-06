# -*- coding: utf-8 -*-
{
    'name': 'Visa History',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Visa History""",
    'description': """
        Adds a list of visa in an opportunity
    """,
    'category': 'Extra Tools',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_visa_type_views.xml',
        'data/mail_template_data.xml',
        'data/ir_action_server_data.xml',
        'data/base_automation_data.xml',
        'data/crm_visa_type_data.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}