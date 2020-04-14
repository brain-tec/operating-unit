# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    operating_unit_id = fields.Many2one(
        'operating.unit',
        compute="_compute_operating_unit_id", store=True,
        string='Source Location Operating Unit',
    )
    operating_unit_dest_id = fields.Many2one(
        'operating.unit',
        compute="_compute_operating_unit_dest_id",
        string='Dest. Location Operating Unit',
    )

    @api.multi
    @api.depends('location_id', 'location_id.operating_unit_id',
                 'picking_type_id', 'picking_type_id.warehouse_id',
                 'picking_type_id.warehouse_id.operating_unit_id')
    def _compute_operating_unit_id(self):
        for item in self:
            # For dropshipping
            item.operating_unit_id = \
                item.location_id.operating_unit_id or \
                item.picking_type_id.warehouse_id.operating_unit_id

    @api.multi
    @api.depends('location_id', 'location_id.operating_unit_id',
                 'picking_type_id', 'picking_type_id.warehouse_id',
                 'picking_type_id.warehouse_id.operating_unit_id')
    def _compute_operating_unit_dest_id(self):
        for item in self:
            item.operating_unit_dest_id = \
                item.location_dest_id.operating_unit_id or \
                item.picking_type_id.warehouse_id.operating_unit_id

    @api.multi
    @api.constrains('picking_id', 'location_id', 'location_dest_id')
    def _check_stock_move_operating_unit(self):
        for stock_move in self:
            ou_pick = stock_move.picking_id.operating_unit_id or False
            ou_src = stock_move.operating_unit_id or False
            ou_dest = stock_move.operating_unit_dest_id or False
            if ou_src and ou_pick and (ou_src != ou_pick) and \
                    (ou_dest != ou_pick):
                raise UserError(_(
                    "Configuration error. The stock move must be related to "
                    "a location (source or destination) that belongs to the "
                    "requesting Operating Unit."))
