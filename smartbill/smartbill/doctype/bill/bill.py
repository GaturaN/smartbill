# Copyright (c) 2024, Gatura Njenga and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe.model.document import Document


class Bill(Document):
	def validate(self):
		validate_type(self)
		validate_amount(self)
		validate_due_date(self)
  		# pass

	
def validate_type(self):
    # make recurring_model mandatory if bill type is recurring
    if self.type == "Recurring Payment":
        if not self.recurring_model:
            frappe.throw("Recurring model is required")
            
            
def validate_amount(self):
    # amount should not be less than 100
    amount = self.amount
    if amount:
        if amount < 100:
            frappe.throw("Bill amount should not be less than 100")
            
def validate_due_date(self):
    # due_date should not be in the past and should be over a week from now
	due_date = getdate(self.due_date)
	if due_date:
		today = getdate()
		if due_date < today:
			frappe.throw("Due date cannot be in the past")
		elif (due_date - today).days < 7:
			frappe.throw("Due date should be at least 7 days from now")
