# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee Equipment",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_terminate_reason",
        "base_print_policy",
        "base_multiple_approval",
        "stock",
        "hr",
        "web_readonly_bypass",
        "base_ir_filters_active",
        "base_action_rule",
        "stock_employee_equipment_operation",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "data/ir_actions_server_data.xml",
        "views/product_template_views.xml",
        "views/hr_equipment_request_type_views.xml",
        "views/hr_equipment_request_reason_views.xml",
        "views/hr_equipment_request_views.xml",
        "views/hr_equipment_request_detail_views.xml",
    ],
    "demo": [
        "demo/hr_equipment_request_reason_demo.xml",
        "demo/hr_equipment_request_type_demo.xml",
        # "demo/account_journal_demo.xml",
        # "demo/account_account_demo.xml",
        # "demo/hr_reimbursement_type_demo.xml",
        "demo/tier_definition_demo.xml",
    ],
}
