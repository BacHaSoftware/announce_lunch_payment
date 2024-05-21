# -*- encoding: utf-8 -*-
{
    'name': "Announce Lunch Payment",
    'version': '1.0',
    'summary': 'Announce Lunch Payment',
    'category': 'Human Resources/Lunch',
    'description': """
        Manage and announce your monthly lunch payments effortlessly. 
        Keep track of all orders and ensure timely payments.
    """,
    "depends": ['lunch'],
    'data': [
        'data/ir_cron_lunch_email.xml',
        'data/email_template_lunch.xml',
        'views/res_config_settings.xml'
    ],
    # Author
    'author': 'Bac Ha Software',
    'website': 'https://bachasoftware.com',
    'maintainer': 'Bac Ha Software',

    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}