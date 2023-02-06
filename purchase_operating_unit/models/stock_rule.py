from odoo import _, models
from odoo.exceptions import UserError


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(self, company_id, origins, values):
        res = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )

        if "group_id" in res:
            so = self.env["procurement.group"].browse(res["group_id"]).sale_id

            if so:
                # We don't rely on the SO having the "operating_unit_id" field;
                # instead, we rely on the warehouse
                # having such a field (this is because of the manifest dependencies)
                so_operating_unit = so.warehouse_id.operating_unit_id
                so_operating_unit_id = so_operating_unit.id

                res.update(
                    {
                        "operating_unit_id": so_operating_unit_id,
                        "requesting_operating_unit_id": so_operating_unit_id,
                    }
                )

                if hasattr(so_operating_unit, "purchase_note"):
                    res.update({"purchase_note": so_operating_unit.purchase_note})

                if "picking_type_id" in res:
                    picking_type_obj = self.env["stock.picking.type"]
                    picking_type = picking_type_obj.browse(res["picking_type_id"])

                    if (
                        picking_type.code != "incoming"
                        or picking_type.warehouse_id.operating_unit_id.id
                        != so_operating_unit_id
                    ):
                        in_picking_types = picking_type_obj.search(
                            [
                                ("code", "=", "incoming"),
                                (
                                    "warehouse_id.operating_unit_id",
                                    "=",
                                    so_operating_unit_id,
                                ),
                            ]
                        )

                        if in_picking_types:
                            res.update({"picking_type_id": in_picking_types[0].id})
                        else:
                            raise UserError(
                                _(
                                    'No Operation Type of type "Receipt" '
                                    'found for the "%s" Operating Unit'
                                )
                                % so_operating_unit.display_name
                            )

        return res
