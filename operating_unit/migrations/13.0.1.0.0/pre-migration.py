# Copyright 2020 Jarsa - Alan Ramos
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl.html).

from openupgradelib import openupgrade

column_renames = {"operating_unit_users_rel": [("poid", "operating_unit_id"),
                                               ("default_operating_unit_id", "operating_unit_default_id")]}


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "operating_unit_users_rel", "poid"):
        openupgrade.rename_columns(env.cr, column_renames)
    if openupgrade.column_exists(env.cr, "operating_unit_users_rel", "default_operating_unit_id"):
        openupgrade.rename_columns(env.cr, column_renames)
