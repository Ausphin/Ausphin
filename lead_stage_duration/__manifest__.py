# -*- coding: utf-8 -*-
{
    'name': 'Lead Stage Duration',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Lead Stage Duration""",
    'description': """
        Creates a list of stages the lead has been to and the following info
        - Start Date
        - End Date
        - Salesperson
        
        Computes the total duration of a lead in a stage
    """,
    'category': 'Extra Tools',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/crm_team_views.xml',
        'views/crm_lead_stage_log_views.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}