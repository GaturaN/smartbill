// Copyright (c) 2024, Gatura Njenga and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
  refresh(frm) {
    // remove fields from display
    frm.toggle_display(
      ["national_id", "passport_number"],
      frm.doc.identification_type !== "Select"
    ); 
    // This has been moved to server side
    // // set full name
    // if (frm.doc.middle_name_optional) {
    //   frm.set_value(
    //     "full_name",
    //     frm.doc.first_name +
    //       " " +
    //       frm.doc.middle_name_optional +
    //       " " +
    //       frm.doc.last_name
    //   );
    // } else {
    //   frm.set_value("full_name", frm.doc.first_name + " " + frm.doc.last_name);
    // }
  },

  validate(frm) {
    if (frm.doc.identification_type === "Select") {
      frappe.throw("Please select an identification type");
    }
    // check if national id is int and valid
    if (frm.doc.national_id) {
      let id = frm.doc.national_id;
      // check if it is not a number
      if (isNaN(id)) {
        frm.set_value("national_id", "");
        frappe.throw("National ID is not valid");
      }
      // check if length is correct
      if (id.length !== 8) {
        frm.set_value("national_id", "");
        frappe.throw("National ID is not valid");
      }
    }
    // check if passport number is valid
    // Since passport numbers are different for different countries, we will only check the length
    // Should not be more than 9 or less than 6
    if (frm.doc.passport_number) {
      if (
        frm.doc.passport_number.length < 6 ||
        frm.doc.passport_number.length > 9
      ) {
        frm.set_value("passport_number", "");
        frappe.throw("Passport number is not valid");
      }
    }
    // check if email is valid
    if (frm.doc.email) {
      if (!frm.doc.email.includes("@")) {
        frm.set_value("email", "");
        frappe.throw("Email is not valid");
      }
    }
  },

  date_of_birth(frm) {
    // check if date of birth is valid
    if (frm.doc.date_of_birth) {
      if (Date.parse(frm.doc.date_of_birth) > Date.now()){
        frappe.msgprint("Date of birth is not valid");
      }
      // calculate age in years, months and days
      let today = new Date();
      let birthDate = new Date(frm.doc.date_of_birth);
      let age = today.getFullYear() - birthDate.getFullYear();
      let month = today.getMonth() - birthDate.getMonth();
      if (month < 0 || (month === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      // write age in years months and days
      frm.set_value(
        "age",
        age +
          " years " +
          month +
          " months " +
          (today.getDate() - birthDate.getDate()) +
          " days"
      );
      // frm.set_value("age", age);
    }
  },

  age(frm) {
    // Check if age > 18
    if (frm.doc.age) {
      if (parseInt(frm.doc.age) < 18) {
        frm.set_value("date_of_birth", "");
        frappe.throw("Must be 18 or older");
      }
    }
  },

  identification_type(frm) {
    if (frm.doc.identification_type === "Select") {
      frm.toggle_display(["national_id", "passport_number"], false);
    } else {
      frm.toggle_display(["national_id", "passport_number"], true);
    }
    // if National id is selected, set national_id to mandatory
    frm.toggle_reqd(
      "national_id",
      frm.doc.identification_type === "National ID"
    );
    // if Passport is selected, set passport_number to mandatory
    frm.toggle_reqd(
      "passport_number",
      frm.doc.identification_type === "Passport"
    );
  },
});
