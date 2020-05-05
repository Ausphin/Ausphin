# -*- coding: utf-8 -*-
{
    'name': 'Activity Reminder',
    'version': '1.0',
    'depends': [
        'mail',
        'base_automation',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Activity Reminder""",
    'description': """
        Send an email when an activity is due tomorrow and today
    """,
    'category': 'Extra Tools',
    'data': [
        'data/mail_template_data.xml',
        'data/base_automation_data.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}