# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

DRAFT_STATE = [
    "draft",
    "confirm",
]


class HrEquipmentRequestDetail(models.Model):
    _name = "hr.equipment_request_detail"
    _description = "Employee Equipment Detail"
    _inherit = [
        "mail.thread",
    ]

    @api.depends(
        "product_id",
        "type_id",
        "employee_id",
        "equipment_placement",
    )
    def _compute_allowed_location_ids(self):
        for record in self:
            result = []
            if (
                record.equipment_placement
                and record.equipment_placement == "employee"
                and record.employee_id
                and record.employee_id.address_id
                and record.employee_id.address_id.property_stock_employee_id
            ):
                location = record.employee_id.address_id.property_stock_employee_id
                result.append(location.id)
            elif (
                record.equipment_placement and record.equipment_placement == "location"
            ):

                if record.product_id and record.product_id.restrict_equipment_location:
                    product = record.product_id
                    result = product.allowed_equipment_location_ids.ids
                else:
                    if record.type_id:
                        result = record.type_id.allowed_location_ids.ids
            record.allowed_location_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_show_equipment_placement(self):
        for record in self:
            record.show_equipment_placement = record.type_id.show_equipment_placement

    @api.depends(
        "type_id",
    )
    def _compute_allowed_route_ids(self):
        for record in self:
            result = []
            if record.type_id:
                result = record.type_id.allowed_route_ids.ids
            record.allowed_route_ids = result

    @api.depends("procurement_id", "procurement_id.move_ids")
    def _compute_move_ids(self):
        for record in self:
            result = []
            if record.procurement_id and record.procurement_id.move_ids:
                result = record.procurement_id.move_ids.ids
            record.move_ids = [(6, 0, result)]

    @api.depends(
        "request_id.state",
        "procurement_id",
        "procurement_id.move_ids",
        "procurement_id.move_ids.state",
    )
    def _compute_state(self):
        for record in self:
            result = "draft"
            if record.request_id.state in DRAFT_STATE:
                result = "draft"
            elif record.request_id.state == "approve":
                result = "plan"
            elif (
                record.request_id.state == "open"
                and record.procurement_id
                and len(record.move_ids.filtered(lambda r: r.state != "done")) != 0
            ):
                result = "open"
            elif (
                record.request_id.state == "open"
                and record.procurement_id
                and len(record.move_ids.filtered(lambda r: r.state != "done")) == 0
            ):
                result = "done"
            elif record.request_id.state == "done":
                result = "done"
            elif record.request_id.state == "cancel":
                result = "cancel"
            record.state = result

    request_id = fields.Many2one(
        string="# Request",
        comodel_name="hr.equipment_request",
        required=True,
        ondelete="cascade",
    )
    type_id = fields.Many2one(
        string="Request Type",
        comodel_name="hr.equipment_request_type",
        related="request_id.type_id",
        store=True,
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        related="request_id.employee_id",
        store=True,
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        related="request_id.department_id",
        store=True,
    )
    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="hr.employee",
        related="request_id.manager_id",
        store=True,
    )
    job_id = fields.Many2one(
        string="Job",
        comodel_name="hr.job",
        related="request_id.job_id",
        store=True,
    )
    show_equipment_placement = fields.Boolean(
        string="Show Equipment Placement",
        compute="_compute_show_equipment_placement",
        store=False,
    )
    name = fields.Text(
        string="Equipment Specification",
        copy=True,
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        copy=False,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "plan": [
                ("readonly", False),
            ],
        },
    )
    equipment_placement = fields.Selection(
        string="Equipment Placement",
        selection=[
            ("employee", "Personal Equipment"),
            ("location", "Specific Location"),
        ],
        default="employee",
        copy=False,
        required=True,
    )
    allowed_location_ids = fields.Many2many(
        string="Allowed Locations",
        comodel_name="stock.location",
        compute="_compute_allowed_location_ids",
        store=False,
    )
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        ondelete="restrict",
        copy=True,
        required=True,
    )
    allowed_route_ids = fields.Many2many(
        string="Allowed Routes",
        comodel_name="stock.location.route",
        compute="_compute_allowed_route_ids",
        store=False,
    )
    route_id = fields.Many2one(
        string="Route",
        comodel_name="stock.location.route",
        copy=False,
        ondelete="restrict",
        readonly=True,
        states={
            "plan": [
                ("readonly", False),
            ],
        },
    )
    procurement_id = fields.Many2one(
        string="Procurement Order",
        comodel_name="procurement.order",
        copy=False,
        readonly=True,
    )
    move_ids = fields.Many2many(
        string="Moves",
        comodel_name="stock.move",
        copy=False,
        relation="rel_equip_req_detail_2_move",
        column1="detail_id",
        column2="move_id",
        compute="_compute_move_ids",
        store=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("plan", "Procurement Planning"),
            ("open", "Waiting for Realization"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
        copy=False,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_name(self):
        self.name = False
        if self.product_id:
            self.name = self.product_id.name
            if self.product_id.description:
                self.name += "\n" + self.product_id.description

    @api.onchange(
        "type_id",
    )
    def onchange_equipment_placement(self):
        if self.type_id:
            self.equipment_placement = self.type_id.default_equipment_placement

    @api.onchange(
        "type_id",
    )
    def onchange_route_id(self):
        self.route_id = False

    @api.multi
    def _create_procurement_order(self):
        self.ensure_one()
        self._check_before_create_procurement_order()
        obj_proc = self.env["procurement.order"]
        proc = obj_proc.create(self._prepare_procurement_order())
        self.write({"procurement_id": proc.id})

    @api.multi
    def _check_before_create_procurement_order(self):
        self.ensure_one()
        result = True

        if not self.product_id:
            error_msg = "Please select product"
            result = False

        if not self.route_id:
            error_msg = "Please select route"
            result = False

        if not result:
            raise UserError(_(error_msg))

        return result

    @api.multi
    def _prepare_procurement_order(self):
        self.ensure_one()
        return {
            "name": self.name,
            "product_id": self.product_id.id,
            "product_uom": self.product_id.uom_id.id,
            "product_qty": 1.0,
            "warehouse_id": False,
            "location_id": self.location_id.id,
            "route_ids": [(6, 0, [self.route_id.id])],
            "origin": self.request_id.name,
            "group_id": self.request_id.procurement_group_id.id,
        }
