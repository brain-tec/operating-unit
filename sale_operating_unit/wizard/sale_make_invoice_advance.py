from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoices(self, sale_orders):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoices(sale_orders)
        invoice.operating_unit_id = sale_orders.operating_unit_id.id
        return invoice
