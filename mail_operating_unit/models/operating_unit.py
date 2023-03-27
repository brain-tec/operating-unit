##############################################################################
# Copyright (c) 2021 brain-tec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.
# See LICENSE file for full licensing details.
##############################################################################

from odoo import fields, models


class OperatingUnit(models.Model):

    _inherit = "operating.unit"

    catchall_alias = fields.Char()
    catchall_domain = fields.Char()
    outgoing_mail_server_id = fields.Many2one("ir.mail_server")
