##############################################################################
# Copyright (c) 2021 brain-tec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.
# See LICENSE file for full licensing details.
##############################################################################

from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    operating_unit_id = fields.Many2one("operating.unit", "Operating Unit")
