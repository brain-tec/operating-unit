##############################################################################
# Copyright (c) 2021 brain-tec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.
# See LICENSE file for full licensing details.
##############################################################################

from odoo import api, fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    operating_unit_id = fields.Many2one("operating.unit")

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        model = result.get("model", False)
        res_id = result.get("res_id", False)
        if model and res_id:
            model_object = self.env[model].browse(res_id)
            if hasattr(model_object, "operating_unit_id"):
                result["operating_unit_id"] = model_object.operating_unit_id.id

                template_id = result.get("template_id", False)
                if template_id and model_object.operating_unit_id:
                    template_obj = self.env["mail.template"]
                    template = template_obj.browse(template_id)
                    if (
                        template.operating_unit_id
                        and template.operating_unit_id != model_object.operating_unit_id
                    ):
                        valid_templates = template_obj.search(
                            [
                                ("model", "=", model),
                                "|",
                                (
                                    "operating_unit_id",
                                    "=",
                                    model_object.operating_unit_id.id,
                                ),
                                ("operating_unit_id", "=", False),
                            ]
                        )
                        if hasattr(template_obj, "sequence"):
                            valid_templates = valid_templates.sorted("sequence")
                        result["template_id"] = (
                            valid_templates and valid_templates[0].id or False
                        )
        return result
