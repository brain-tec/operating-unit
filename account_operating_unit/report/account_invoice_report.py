# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'

    operating_unit_id = fields.Many2one('operating.unit',
                                        string='Operating Unit')

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", move.operating_unit_id as operating_unit_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", move.operating_unit_id"
