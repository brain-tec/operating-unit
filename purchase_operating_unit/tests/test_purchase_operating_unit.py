# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import time

from odoo.exceptions import ValidationError
from odoo.tests import Form, common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TestPurchaseOperatingUnit(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResUsers = cls.env["res.users"]
        cls.PurchaseOrder = cls.env["purchase.order"]
        cls.AccountInvoice = cls.env["account.move"]
        cls.AccountAccount = cls.env["account.account"]
        # company
        cls.company = cls.env.ref("base.main_company")
        # groups
        cls.group_purchase_user = cls.env.ref("purchase.group_purchase_user")
        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        cls.b2b = cls.env.ref("operating_unit.b2b_operating_unit")
        # Partner
        cls.partner1 = cls.env.ref("base.res_partner_1")
        # Products
        cls.product1 = cls.env.ref("product.product_product_7")
        cls.product2 = cls.env.ref("product.product_product_9")
        cls.product3 = cls.env.ref("product.product_product_11")
        # Account
        payable_acc_type = cls.env.ref("account.data_account_type_payable").id
        cls.account = cls.AccountAccount.search(
            [("user_type_id", "=", payable_acc_type)], limit=1
        )
        # Create users
        cls.user1_id = cls._create_user(
            "user_1",
            [cls.group_purchase_user],
            cls.company,
            [cls.ou1],
        )
        cls.user2_id = cls._create_user(
            "user_2",
            [cls.group_purchase_user],
            cls.company,
            [cls.b2b],
        )
        cls.purchase1 = cls._create_purchase(
            cls.user1_id,
            [(cls.product1, 1000), (cls.product2, 500), (cls.product3, 800)],
        )
        cls.purchase1.with_user(cls.user1_id).button_confirm()
        cls.invoice = cls._create_invoice(cls.purchase1, cls.partner1, cls.account)

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.ResUsers.with_context(**{"no_reset_password": True}).create(
            {
                "name": "Chicago Purchase User",
                "login": login,
                "password": "demo",
                "email": "chicago@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user.id

    def _create_purchase(self, user_id, line_products):
        """Create a purchase order.
        ``line_products`` is a list of tuple [(product, qty)]
        """
        lines = []
        for product, qty in line_products:
            line_values = {
                "name": product.name,
                "product_id": product.id,
                "product_qty": qty,
                "product_uom": product.uom_id.id,
                "price_unit": 50,
                "date_planned": time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            }
            lines.append((0, 0, line_values))
        purchase = self.PurchaseOrder.with_user(user_id).create(
            {
                "operating_unit_id": self.ou1.id,
                "requesting_operating_unit_id": self.ou1.id,
                "partner_id": self.partner1.id,
                "order_line": lines,
                "company_id": self.company.id,
            }
        )
        return purchase

    def _create_invoice(self, purchase, partner, account):
        """Create a vendor invoice for the purchase order."""
        invoice_vals = {
            "purchase_id": purchase.id,
            "partner_id": partner.id,
            "move_type": "in_invoice",
        }
        purchase_context = {
            "active_id": purchase.id,
            "active_ids": purchase.ids,
            "active_model": "purchase.order",
        }
        res = (
            self.env["account.move"]
            .with_context(**purchase_context)
            .create(invoice_vals)
        )
        return res

    def test_01_purchase_operating_unit(self):
        self.purchase1.button_cancel()
        self.purchase1.button_draft()
        # Check change operating unit in purchase
        with self.assertRaises(ValidationError):
            self.b2b.company_id = False
            with Form(self.purchase1) as po:
                po.operating_unit_id = self.b2b
        self.purchase1.with_user(self.user1_id).button_confirm()
        # Create Vendor Bill
        f = Form(self.env["account.move"].with_context(default_move_type="in_invoice"))
        f.partner_id = self.purchase1.partner_id
        f.purchase_id = self.purchase1
        invoice = f.save()
        self.assertEqual(invoice.operating_unit_id, self.purchase1.operating_unit_id)
        self.assertEqual(
            invoice.invoice_line_ids[0].operating_unit_id,
            invoice.invoice_line_ids[0].purchase_line_id.operating_unit_id,
        )
        # Check change operating unit in invoice line != purchase line,
        # it should error.
        with self.assertRaises(ValidationError):
            with Form(invoice.invoice_line_ids[0]) as line:
                line.operating_unit_id = self.b2b
