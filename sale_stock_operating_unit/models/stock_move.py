# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        """
        Override to add Operating Units to Picking.
        """
        values = super(StockMove, self)._get_new_picking_values()
        # Adding operating_unit_id as for 2 steps deliveries/receipts,
        # one of the pickings is not associated to the sale line
        values.update(
            {
                "operating_unit_id": self.sale_line_id.operating_unit_id.id
                or self.operating_unit_id.id
            }
        )

        return values
