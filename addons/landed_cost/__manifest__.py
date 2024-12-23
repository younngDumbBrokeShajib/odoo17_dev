# -*- coding: utf-8 -*-
{
    'name': "landedCost",

    'summary': "Landed Cost",

    'description': """
To use this feature be sure to install sales app as to use this. Be sure to add CD,SD,RD,VAT,AIT,AT from the product template.
    """,

    'author': "Shajib Hossain, Informax Tech LTD",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/landed_cost_form_view.xml',
        'security/ir.model.access.csv',
        'reports/landed_cost_report.xml',
        'views/product_template_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "installable": True,
    "installable":True,
}


