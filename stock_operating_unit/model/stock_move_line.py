# © 2020 brain-tec group
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        compute="_compute_operating_unit_id",
        store=True,
        string="Source Location Operating Unit",
    )

    operating_unit_dest_id = fields.Many2one(
        "operating.unit",
        compute="_compute_operating_unit_dest_id",
        store=True,
        string="Dest. Location Operating Unit",
    )

    @api.depends(
        "location_id",
        "location_id.operating_unit_id",
        "picking_id.picking_type_id.warehouse_id.operating_unit_id",
    )
    def _compute_operating_unit_id(self):
        for rec in self:
            rec.operating_unit_id = (
                rec.location_id.operating_unit_id
                or rec.picking_id.picking_type_id.warehouse_id.operating_unit_id
            )

    @api.depends(
        "location_dest_id",
        "location_dest_id.operating_unit_id",
        "picking_id.picking_type_id.warehouse_id.operating_unit_id",
    )
    def _compute_operating_unit_dest_id(self):
        for rec in self:
            rec.operating_unit_dest_id = (
                rec.location_dest_id.operating_unit_id
                or rec.picking_id.picking_type_id.warehouse_id.operating_unit_id
            )

    @api.constrains("picking_id", "location_id", "location_dest_id")
    def _check_operating_units(self):
        for rec in self:
            ou_pick = rec.picking_id.operating_unit_id
            ou_src = rec.operating_unit_id
            ou_dest = rec.operating_unit_dest_id
            if ou_src and ou_pick and (ou_src != ou_pick) and (ou_dest != ou_pick):
                raise UserError(
                    _(
                        "Configuration error. The Product Moves must "
                        "be related to locations (source and destination) "
                        "that belong to the requesting Operating Unit."
                    )
                )
