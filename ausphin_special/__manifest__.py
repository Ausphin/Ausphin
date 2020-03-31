# -*- coding: utf-8 -*-
{
    'name': 'Ausphin Special',
    'version': '0.1',
    'depends': [
        'crm',
        'kanban_draggable',
        'crm_team_sequence',
        'lead_stage_duration',
        'tenureship',
        'visa_history',
        'crm_site',
        'crm_training',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Special Modifications for Ausphin""",
    'description': """
        Special Modifications for Ausphin
    """,
    'category': 'Special',
    'data': [
        'security/crm_lead_security.sql',
        'security/crm_lead_security.xml',
        'security/crm_team_security.xml',
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml',
        'views/crm_stage_views.xml',
        'wizards/crm_lead2opportunity_partner_views.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}