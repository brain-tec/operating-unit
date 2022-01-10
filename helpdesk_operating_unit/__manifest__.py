##############################################################################
# Copyright (c) 2022 brain-tec AG (https://braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
{
    "name": "Operating Unit for Helpdesk",
    "summary": "Operating Unit for Helpdesk",
    "version": "13.0.1.0.0",
    "category": "Operations/Helpdesk",
    "author": "brain-tec AG, " "Odoo Community Association (OCA)",
    "website": "www.bt-group.com",
    "license": "AGPL-3",
    "depends": ["operating_unit", "helpdesk"],
    "data": ["security/ir_rule.xml", "views/helpdesk_ticket.xml"],
    "application": False,
    "installable": True,
    "auto_install": False,
}
