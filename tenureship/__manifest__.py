# -*- coding: utf-8 -*-
{
    'name': 'Tenureship Calculation',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Tenureship Calculation""",
    'description': """
        Calculates the tenureship of an opportunity
        based on the field specified in the sales team if any
    """,
    'category': 'Extra Tools',
    'data': [
        'views/crm_team_views.xml',
        'views/crm_lead_views.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}