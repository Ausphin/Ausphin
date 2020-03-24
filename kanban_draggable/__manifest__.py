# -*- coding: utf-8 -*-
{
    'name': 'Kanban Drag Drop Control',
    'version': '0.1',
    'depends': [
        'web',
    ],
    'external_dependencies': {},
    'author': 'Rainier King, '
              'Odev Solutions',
    'website': 'https://odevsolutions.com',
    'summary': """Kanban Drag Drop Control""",
    'description': """
        Provides ability to control drag drop and sorting behavior in kanban views

        Inspired from the public module by Navybits
        https://github.com/Navybits/kanban_draggable
        
        However since they do not have a version for Odoo 12 so we created a copy
    """,
    'category': 'Extra Tools',
    'data': [
        'views/assets.xml',
    ],
    'qweb': [],
    'css': [],
    'images': [],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}