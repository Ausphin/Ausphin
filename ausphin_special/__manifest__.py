# -*- coding: utf-8 -*-
{
    'name': 'Ausphin Special',
    'version': '0.1',
    'depends': [
        'crm',
        'kanban_draggable',
        'crm_move_stage_button',
        'crm_team_sequence',
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
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml',
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