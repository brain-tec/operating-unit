# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends("journal_id")
    def _compute_operating_unit_id(self):
        for payment in self:
            if payment.journal_id:
                payment.operating_unit_id = payment.journal_id.operating_unit_id

    operating_unit_id = fields.Many2one(
        "operating.unit",
        domain="[('user_ids', '=', uid)]",
        compute="_compute_operating_unit_id",
        store=True,
    )

    def _prepare_payment_moves(self):
        res = super(AccountPayment, self)._prepare_payment_moves()
        if not self.operating_unit_id:
            return res
        for move in res:
            journal = self.env["account.journal"].browse(move["journal_id"])
            ou_id = journal.operating_unit_id.id
            move["operating_unit_id"] = ou_id
            for line in move["line_ids"]:
                line[2]["operating_unit_id"] = ou_id
        return res
