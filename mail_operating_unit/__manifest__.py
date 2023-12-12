##############################################################################
# Copyright (c) 2021 brain-tec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.
# See LICENSE file for full licensing details.
##############################################################################

{
    "name": "Mail Operating Unit",
    "summary": "Adds the concept of operating unit (OU) according mail",
    "license": "LGPL-3",
    "version": "15.0.1.0.0",
    "author": "brain-tec AG, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Purchase Management",
    "depends": ["operating_unit", "mail"],
    "data": [
        "data/mail_data.xml",
        "security/mail_alias_security.xml",
        "security/mail_template_security.xml",
        "security/ir.model.access.csv",
        "views/operating_unit_views.xml",
        "views/mail_alias_views.xml",
        "views/mail_template_views.xml",
        "views/res_users_view.xml",
        "wizard/mail_compose_message_view.xml",
    ],
    "installable": True,
}
