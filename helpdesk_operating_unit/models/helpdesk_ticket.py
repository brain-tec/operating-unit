##############################################################################
# Copyright (c) 2022 brain-tec AG (https://braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################

from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    operating_unit_id = fields.Many2one("operating.unit")
