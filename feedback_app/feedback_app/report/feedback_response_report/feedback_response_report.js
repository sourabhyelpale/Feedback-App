// Copyright (c) 2026, QTPL and contributors
// For license information, please see license.txt

frappe.query_reports["Feedback Response Report"] = {
   filters: [

        {
            fieldname: "feedback_master",
            label: "Feedback Master",
            fieldtype: "Link",
            options: "Feedback Master",
            reqd: 1,
            width: 180,
            get_query: function() {
                return {
                    filters: { is_active: 1 }
                };
            }
        },

        {
            fieldname: "project",
            label: "Project",
            fieldtype: "Link",
            options: "Project",
            width: 130
        },

        {
            fieldname: "site_name",
            label: "Site",
            fieldtype: "Link",
            options: "Site",
            width: 120
        },

        {
            fieldname: "user",
            label: "User",
            fieldtype: "Link",
            options: "User",
            width: 130
        },

        {
            fieldname: "trainer",
            label: "Trainer",
            fieldtype: "Link",
            options: "User",
            width: 130
        },

        {
            fieldname: "from_date",
            label: "From",
            fieldtype: "Date",
            width: 110
        },

        {
            fieldname: "to_date",
            label: "To",
            fieldtype: "Date",
            width: 110
        }

    ],

    onload: function(report) {

        report.page.add_inner_button("Download Excel", function() {

            let dialog = new frappe.ui.Dialog({
                title: "Download Excel",
                fields: [
                    {
                        label: "File Name",
                        fieldname: "file_name",
                        fieldtype: "Data",
                        reqd: 1
                    }
                ],
                primary_action_label: "Download",
                primary_action(values) {

                    let filters = report.get_values();

                    let url = frappe.urllib.get_full_url(
                        "/api/method/feedback_app.feedback_app.report.feedback_response_report.feedback_response_report.download_excel"
                        + "?filters=" + encodeURIComponent(JSON.stringify(filters))
                        + "&file_name=" + encodeURIComponent(values.file_name)
                    );

                    window.open(url);

                    dialog.hide();
                }
            });

            dialog.show();

        });

    }
};