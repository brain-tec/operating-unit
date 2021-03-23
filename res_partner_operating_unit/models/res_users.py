# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# Copyright (C) 2019 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.partner_id.operating_unit_ids |= res.operating_unit_default_id
        res.partner_id.operating_unit_ids |= res.operating_unit_ids
        self._check_partner_operating_unit()
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        for user in self:
            if vals.get('operating_unit_default_id'):
                user.partner_id.operating_unit_ids |= user.operating_unit_default_id
                user._check_partner_operating_unit()
            if vals.get('operating_unit_ids'):
                user.partner_id.operating_unit_ids |= user.operating_unit_ids
        return res

    def _check_partner_operating_unit(self):
        if self.partner_id.operating_unit_ids and \
                self.operating_unit_default_id.id not in \
                self.partner_id.operating_unit_ids.ids:
            raise UserError(_(
                "The operating units of the partner must include the default "
                "one of the user."))
