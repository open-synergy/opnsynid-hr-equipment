# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrEquipmentRequestType(models.Model):
    _name = "hr.equipment_request_type"
    _description = "Employee Equipment Request Type"
    _order = "sequence, id"

    name = fields.Char(
        string="Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    default_equipment_placement = fields.Selection(
        string="Default Equipment Placement",
        selection=[
            ("employee", "Personal Equipment"),
            ("location", "Specific Location"),
        ],
        default="employee",
        required=True,
    )
    show_equipment_placement = fields.Boolean(
        string="Show Equipment Placement",
        default=True,
    )
    allowed_location_ids = fields.Many2many(
        string="Allowed Locations",
        comodel_name="stock.location",
        relation="rel_equipment_req_type_2_location",
        column1="type_id",
        column2="location_id",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_equipment_req_type_2_product_categ",
        column1="type_id",
        column2="category_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        relation="rel_equipment_req_type_2_product",
        column1="type_id",
        column2="product_id",
    )
    allowed_route_ids = fields.Many2many(
        string="Allowed Routes",
        comodel_name="stock.location.route",
        relation="rel_equipment_req_type_2_route",
        column1="type_id",
        column2="route_id",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm",
        comodel_name="res.groups",
        relation="rel_confirm_equip_request",
        column1="type_id",
        column2="group_id",
    )
    open_grp_ids = fields.Many2many(
        string="Allow To Open",
        comodel_name="res.groups",
        relation="rel_open_equip_request",
        column1="type_id",
        column2="group_id",
    )
    done_grp_ids = fields.Many2many(
        string="Allow To Finish",
        comodel_name="res.groups",
        relation="rel_done_equip_request",
        column1="type_id",
        column2="group_id",
    )
    restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval",
        comodel_name="res.groups",
        relation="rel_restart_approval_equip_request",
        column1="type_id",
        column2="group_id",
    )
    cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel",
        comodel_name="res.groups",
        relation="rel_cancel_equip_request",
        column1="type_id",
        column2="group_id",
    )
    restart_grp_ids = fields.Many2many(
        string="Allow To Restart",
        comodel_name="res.groups",
        relation="rel_restart_equip_request",
        column1="type_id",
        column2="group_id",
    )
