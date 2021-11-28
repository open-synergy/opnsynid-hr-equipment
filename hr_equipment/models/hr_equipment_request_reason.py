# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrEquipmentRequestReason(models.Model):
    _name = "hr.equipment_request_reason"
    _description = "Employee Equipment Request Reason"
    _order = "sequence, id"

    name = fields.Char(
        string="Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
    )
    note = fields.Text(
        string="Note",
    )
