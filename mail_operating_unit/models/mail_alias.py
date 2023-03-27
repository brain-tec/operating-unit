##############################################################################
# Copyright (c) 2021 brain-tec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.
# See LICENSE file for full licensing details.
##############################################################################

from odoo import api, fields, models


class MailAlias(models.Model):
    _inherit = "mail.alias"

    operating_unit_id = fields.Many2one("operating.unit", "Operating Unit")

    @api.depends('alias_name', 'operating_unit_id', 'operating_unit_id.catchall_domain')
    def _compute_alias_domain(self):
        super()._compute_alias_domain()
        for record in self:
            if record.operating_unit_id:
                record.alias_domain = record.operating_unit_id.catchall_domain
