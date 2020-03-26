# -*- coding: utf-8 -*-
{
    'name': 'Sales Team Sequence',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Sales Team Sequence""",
    'description': """
        Add sequence field for Sales Team
        Sets the default order of sales teams to use sequence
    """,
    'category': 'Extra Tools',
    'data': [
        'views/crm_team_views.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}