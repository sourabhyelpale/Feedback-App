# Copyright (c) 2026, QTPL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FeedbackMaster(Document):
	def validate(self):

		if self.is_active:

			previous = frappe.get_all(
				"Feedback Master",
				filters={
					"form_name": self.form_name,
					"name": ["!=", self.name],
					"is_active": 1
				},
				pluck="name"
			)

			for doc in previous:
				frappe.db.set_value("Feedback Master", doc, "is_active", 0)
