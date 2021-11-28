# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    restrict_equipment_location = fields.Boolean(
        string="Restrict Equipment Location",
        default=False,
    )
    allowed_equipment_location_ids = fields.Many2many(
        string="Allowed Equipment Locations",
        comodel_name="stock.location",
        relation="rel_product_template_2_equipment_loc",
        column1="product_tmpl_id",
        column2="location_id",
    )
