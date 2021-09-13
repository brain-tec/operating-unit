# © 2021 brain-tec AG
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock and Product with Operating Units (Bridge)",
    "summary": "Adds rules for lot and quant to deal with the concept of operating unit (OU) "
               "in stock management and product",
    "version": "13.0.1.0.0",
    "category": "Generic Modules/Sales & Purchases",
    "author": "brain-tec AG, "
    "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["stock_operating_unit", "product_operating_unit"],
    "data": ["security/stock_security.xml"],
    "demo": [],
    "installable": True,
    "auto_install": True,
}
