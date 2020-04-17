# -*- coding: utf-8 -*-
{
    'name': 'CRM Documents',
    'version': '0.1',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """CRM Documents""",
    'description': """
        Major and minor documents for an opportunity
    """,
    'category': 'Extra Tools',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_document_views.xml',
        'views/crm_lead_document_views.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}