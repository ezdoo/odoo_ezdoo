# -*- coding: utf-8 -*-
{
    'name': "website_custom_assets",

    'summary': """
        Inject custom assets to website, stylesheets and javascripts
    """,

    'description': """
        Injects custom javascripts and stylesheets to your website

    """,

    'author': "BarraDev Consulting",
    'website': "http://www.barradev.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}
