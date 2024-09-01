// Copyright (c) 2024, Gatura Njenga and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bill", {
	// refresh(frm) {

	// },
    validate(frm){
        // amount should not be less than 100
        if (frm.doc.amount < 100) {
            frappe.throw ("Amount should not be less than 100");
        }
    },

    type(frm){
        // if type is recurring, show recurring model
        frm.toggle_display(["recurring_model"], frm.doc.type === "Recurring Payment");
        frm.toggle_reqd(["recurring_model"], frm.doc.type === "Recurring Payment");
    }
});
