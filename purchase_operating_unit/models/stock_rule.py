from odoo import _, models
from odoo.exceptions import UserError


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(self, company_id, origins, values):
        res = super()._prepare_purchase_order(company_id, origins, values)
        if origins and "SO" in origins:
            operating_unit = (
                self.env["sale.order"]
                .search([("name", "=", origins)])
                .warehouse_id.operating_unit_id
            )

            res.update(
                {
                    "operating_unit_id": operating_unit.id,
                    "requesting_operating_unit_id": operating_unit.id,
                }
            )

            if hasattr(operating_unit, "purchase_note"):
                res.update({"purchase_note": operating_unit.purchase_note})

            if "picking_type_id" in res:
                type_obj = self.env["stock.picking.type"]
                picking_type = type_obj.browse(res["picking_type_id"])
                if (
                    picking_type.code != "incoming"
                    or picking_type.warehouse_id.operating_unit_id.id
                    != operating_unit.id
                ):

                    # Code copied from _onchange_operating_unit_id in
                    # purchase_order.py
                    types = type_obj.search(
                        [
                            ("code", "=", "incoming"),
                            ("warehouse_id.operating_unit_id", "=", operating_unit.id),
                        ]
                    )
                    if types:
                        res.update({"picking_type_id": types[:1].id})
                    else:
                        raise UserError(
                            _(
                                "No Warehouse found with the Operating Unit "
                                "indicated in the Purchase Order"
                            )
                        )

        return res
