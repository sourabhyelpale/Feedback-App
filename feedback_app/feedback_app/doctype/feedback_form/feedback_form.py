# Copyright (c) 2026, QTPL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FeedbackForm(Document):
    def on_submit(self):

        df = frappe.get_doc("Feedback Master",self.feedback_master)

        ct_length = len(self.feedback_answer)
        df_ct_length = len(df.feedback_question)

        if(ct_length != df_ct_length):
            frappe.throw("Please give answer of all questions")

        doc = frappe.new_doc("Feedback Response")
        doc.feedback_test = self.name
        doc.feedback_master = self.feedback_master
        doc.user = frappe.session.user
        doc.submitted_date = self.date
        doc.project = self.project
        doc.module_type = df.module_type
        doc.doctype_name = df.doctype_name
        doc.site_name = self.site_name
        doc.name1 = self.name1
        doc.email = self.email
        doc.contact_no = self.contact_no

        for response in self.feedback_answer:

            doc.append("feedback_answers", {
                "question" : response.question,
                "answer": response.answer
            })

        doc.insert(ignore_permissions=True)
        doc.submit()

        
