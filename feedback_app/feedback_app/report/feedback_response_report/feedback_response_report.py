# Copyright (c) 2026, QTPL and contributors
# For license information, please see license.txt
import frappe
from frappe.utils.xlsxutils import make_xlsx
from frappe.utils.file_manager import save_file

def execute(filters=None):

    if not filters.get("feedback_master"):
        frappe.throw("Feedback Master is mandatory")

    questions = frappe.get_all(
        "Feedback Question",
        filters={"parent": filters.feedback_master},
        fields=["question"],
        order_by="idx"
    )

    columns = get_columns(questions)
    data = get_data(filters, questions)

    return columns, data


def get_columns(questions):

    columns = [
        {"label": "User", "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Site Name", "fieldname": "site_name", "fieldtype": "Data", "width": 150},
        {"label": "Submitted Date", "fieldname": "submitted_date", "fieldtype": "Datetime", "width": 180},
    ]

    for q in questions:
        columns.append({
            "label": q.question,
            "fieldname": frappe.scrub(q.question),
            "fieldtype": "Data",
            "width": 200
        })

    return columns


def get_data(filters, questions):

    conditions = ""

    if filters.get("project"):
        conditions += " AND fr.project = %(project)s"

    if filters.get("site_name"):
        conditions += " AND fr.site_name = %(site_name)s"

    if filters.get("user"):
        conditions += " AND fr.user = %(user)s"
    
    if filters.get("trainer"):
        conditions += " AND fr.trainer = %(trainer)s"

    if filters.get("from_date"):
        conditions += " AND DATE(fr.submitted_date) >= %(from_date)s"

    if filters.get("to_date"):
        conditions += " AND DATE(fr.submitted_date) <= %(to_date)s"

    responses = frappe.db.sql(f"""
        SELECT
            fr.name,
            fr.user,
            fr.project,
            fr.site_name,
            fr.submitted_date,
            fr.feedback_master,
            fa.question,
            fa.answer
        FROM
            `tabFeedback Response` fr
        LEFT JOIN
            `tabFeedback Answer` fa
        ON
            fa.parent = fr.name
        WHERE
            fr.docstatus = 1
            AND fr.feedback_master = %(feedback_master)s
            {conditions}
        ORDER BY fr.submitted_date DESC
    """, filters, as_dict=1)

    result = {}

    for row in responses:

        if row.name not in result:
            result[row.name] = {
                "user": row.user,
                "project": row.project,
                "site_name": row.site_name,
                "submitted_date": row.submitted_date
            }

        if row.question:
            result[row.name][frappe.scrub(row.question)] = row.answer

    return list(result.values())


@frappe.whitelist()
def download_excel(filters=None, file_name="feedback_report"):

    filters = frappe.parse_json(filters)

    columns, data = execute(filters)

    headers = [col["label"] for col in columns]

    excel_data = [headers]

    for row in data:
        excel_data.append([row.get(col["fieldname"]) for col in columns])

    xlsx_file = make_xlsx(excel_data, file_name)

    frappe.response["filename"] = file_name + ".xlsx"
    frappe.response["filecontent"] = xlsx_file.getvalue()
    frappe.response["type"] = "binary"