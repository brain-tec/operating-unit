##############################################################################
# Copyright (c) 2021 braintec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the AGPL-3.0 (http://www.gnu.org/licenses/agpl.html)
# See LICENSE file for full licensing details.
##############################################################################

{
    "name": "Stock and Product with Operating Units (Bridge)",
    "version": "15.0.1.0.0",
    "summary": "Adds rules for lot and quant to deal with the concept of operating unit (OU)"
               " in stock management and product",
    "category": "Generic Modules/Sales & Purchases",
    "author": "braintec AG, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "license": "AGPL-3",
    "depends": ["stock_operating_unit", "product_operating_unit"],
    "data": ["security/stock_security.xml"],
    "installable": True,
    "auto_install": True,
}
