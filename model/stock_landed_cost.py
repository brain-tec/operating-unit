from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero

from odoo.addons.stock_landed_costs.models.stock_landed_cost \
    import LandedCost as LandedCost

import logging
_logger = logging.getLogger(__name__)


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    @api.model
    def _default_operating_unit(self):
        return self.env.user.operating_unit_default_id

    @api.model
    def _default_show_operating_unit(self):
        return len(self.env.user.operating_unit_ids) > 1

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=_default_operating_unit
    )

    show_operating_unit = fields.Boolean(
        compute="_compute_show_operating_unit",
        default="_default_show_operating_unit")

    def _compute_show_operating_unit(self):
        for item in self:
            item.show_operating_unit = \
                len(self.env.user.operating_unit_ids) > 1

    def _register_hook(self):
        """ MonkeyPatch method only when module is installed on the DB.
        The patched method is a copy of standard name_get adding name2.
        The original function pointer to name_get is stored in 'origin'
        attribute.
        The patch need to be removed when module is uninstalled. This is
        done in the uninstall hook during runtime. No server restart
        needed.

        """
        res = super(StockLandedCost, self)._register_hook()

        def button_validate(self):
            if any(cost.state != 'draft' for cost in self):
                raise UserError(_('Only draft landed costs can be validated'))
            if not all(cost.picking_ids for cost in self):
                raise UserError(_('Please define the transfers on which those additional costs should apply.'))
            cost_without_adjusment_lines = self.filtered(lambda c: not c.valuation_adjustment_lines)
            if cost_without_adjusment_lines:
                cost_without_adjusment_lines.compute_landed_cost()
            if not self._check_sum():
                raise UserError(
                    _('Cost and adjustments lines do not match. You should maybe recompute the landed costs.'))

            for cost in self:
                move = self.env['account.move']
                ##########################################################
                # hack by mara1 - Adding operating unit
                move_vals = {
                    'journal_id': cost.account_journal_id.id,
                    'date': cost.date,
                    'ref': cost.name,
                    'line_ids': [],
                    'type': 'entry',
                    'operating_unit_id': cost.operating_unit_id.id
                }
                ##########################################################
                valuation_layer_ids = []
                for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
                    remaining_qty = sum(line.move_id.stock_valuation_layer_ids.mapped('remaining_qty'))
                    linked_layer = line.move_id.stock_valuation_layer_ids[:1]

                    # Prorate the value at what's still in stock
                    cost_to_add = (remaining_qty / line.move_id.product_qty) * line.additional_landed_cost
                    if not cost.company_id.currency_id.is_zero(cost_to_add):
                        valuation_layer = self.env['stock.valuation.layer'].create({
                            'value': cost_to_add,
                            'unit_cost': 0,
                            'quantity': 0,
                            'remaining_qty': 0,
                            'stock_valuation_layer_id': linked_layer.id,
                            'description': cost.name,
                            'stock_move_id': line.move_id.id,
                            'product_id': line.move_id.product_id.id,
                            'stock_landed_cost_id': cost.id,
                            'company_id': cost.company_id.id,
                        })
                        linked_layer.remaining_value += cost_to_add
                        valuation_layer_ids.append(valuation_layer.id)
                    # Update the AVCO
                    product = line.move_id.product_id
                    if product.cost_method == 'average' and not float_is_zero(product.quantity_svl,
                                                                              precision_rounding=product.uom_id.rounding):
                        product.with_context(force_company=self.company_id.id).sudo().\
                            standard_price += cost_to_add / product.quantity_svl
                    # `remaining_qty` is negative if the move is out and delivered proudcts that were not
                    # in stock.
                    qty_out = 0
                    if line.move_id._is_in():
                        qty_out = line.move_id.product_qty - remaining_qty
                    elif line.move_id._is_out():
                        qty_out = line.move_id.product_qty
                    move_vals['line_ids'] += line._create_accounting_entries(move, qty_out)

                move_vals['stock_valuation_layer_ids'] = [(6, None, valuation_layer_ids)]
                move = move.create(move_vals)
                cost.write({'state': 'done', 'account_move_id': move.id})
                move.post()

                if (cost.vendor_bill_id and cost.vendor_bill_id.state == 'posted' and
                        cost.company_id.anglo_saxon_accounting):
                    all_amls = cost.vendor_bill_id.line_ids | cost.account_move_id.line_ids
                    for product in cost.cost_lines.product_id:
                        accounts = product.product_tmpl_id.get_product_accounts()
                        input_account = accounts['stock_input']
                        all_amls.filtered(
                            lambda aml: aml.account_id == input_account and not aml.full_reconcile_id).reconcile()
            return True

        origin = getattr(LandedCost.button_validate, 'origin', None)
        if origin != button_validate:
            LandedCost._patch_method('button_validate', button_validate)
            _logger.info('LandedCost.button_validate method'
                         ' patched to add operating unit!')

        return res
