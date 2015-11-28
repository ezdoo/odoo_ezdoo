{
    'name': 'Website Maintenance',
    'version': '1.0',
    'category': 'Website',
    'description': """This module handle the maintenance for Odoo website.""",
    'author': 'BarraDev Consulting',
    'website': 'www.barradev.com',
    'summary': 'Turn your site offline when you need.',
    'license': 'AGPL-3',
    'depends': ['website'],
    'data': [
        'view/website_maintenance_templates.xml',
        'view/res_config.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
