# -*- coding: utf-8 -*-
{
    'name': 'Move Opportunity Stage Using Button',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Move Opportunity Stage Using Button""",
    'description': """
        Replace default method of changing stages to use button
        
        1 button for moving to next
        1 button for moving to previous
        
        Next and previous stages will be determined by the sequence of the stages
    """,
    'category': '',
    'data': [
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