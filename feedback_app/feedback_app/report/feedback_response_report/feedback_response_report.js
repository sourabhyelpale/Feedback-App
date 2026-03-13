// Copyright (c) 2026, QTPL and contributors
// For license information, please see license.txt

frappe.query_reports["Feedback Response Report"] = {
    filters: [

        {
            fieldname: "feedback_master",
            label: "Feedback Master",
            fieldtype: "Link",
            options: "Feedback Master",
            reqd: 1
        },

        {
            fieldname: "project",
            label: "Project",
            fieldtype: "Link",
            options: "Project"
        },

        {
            fieldname: "site_name",
            label: "Site Name",
            fieldtype: "Link",
			options: "Site"
        },

        {
            fieldname: "user",
            label: "User",
            fieldtype: "Link",
            options: "User"
        },

        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date"
        },

        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date"
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