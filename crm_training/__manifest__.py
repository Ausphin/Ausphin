# -*- coding: utf-8 -*-
{
    'name': 'Training',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Training""",
    'description': """
        Allows managing of training venues
        Adds field in Lead/Opportunity for related training
    """,
    'category': 'Extra Tools',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_training_menus.xml',
        'views/crm_training_views.xml',
        'views/crm_training_venue_views.xml',
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