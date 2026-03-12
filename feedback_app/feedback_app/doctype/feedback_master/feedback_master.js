// Copyright (c) 2026, QTPL and contributors
// For license information, please see license.txt

frappe.ui.form.on('Feedback Master', {
    module_type: function(frm) {

        if (frm.doc.module_type) {

            frm.set_query("doctype_name", function() {
                return {
                    filters: {
                        module: frm.doc.module_type
                    }
                };
            });

        }

    }
});
