# -*- coding: utf-8 -*-
{
    'name': 'Lead/Opportunity Sites',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Lead/Opportunity Sites""",
    'description': """
        Specify which site a lead belongs to
    """,
    'category': 'Extra Tools',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_site_views.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}