# © 2019 brain-tec AG
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.tests import common


class OperatingUnitsTransactionCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(OperatingUnitsTransactionCase, cls).setUpClass()

    @classmethod
    def _create_user(cls, login, groups, company, operating_units):
        group_ids = [group.id for group in groups]
        default_ou_id = False if not operating_units else operating_units[0].id
        user = (
            cls.env["res.users"]
            .with_context({"no_reset_password": True})
            .create(
                {
                    "name": "Test User",
                    "login": login,
                    "password": "demo",
                    "email": "test@yourcompany.com",
                    "company_id": company.id,
                    "company_ids": [(4, company.id)],
                    "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                    "operating_unit_default_id": default_ou_id,
                    "groups_id": [(6, 0, group_ids)],
                }
            )
        )
        return user
