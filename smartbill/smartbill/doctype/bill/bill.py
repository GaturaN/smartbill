# Copyright (c) 2024, Gatura Njenga and contributors
# For license information, please see license.txt

import frappe
import math
from frappe.utils import getdate
from frappe.model.document import Document


class Bill(Document):
	def validate(self):
		validate_type(self)
		validate_amount(self)
		validate_due_date(self)
		set_deposit_amount(self)
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
   
"""
This sections is going to set the deposit_amount based on the financing_plan, amount, and due_date.
if plan is once, set deposit to bill mount
if daily, get number of days between now and due date => set deposit to bill mount / number of days
if weekly, ensure due date is more than a week from now => get number of weeks between now and due date => set deposit to bill mount / number of weeks
if monthly, ensure due date is more than a month from now => get number of months between now and due date => set deposit to bill mount / number of months
"""

def set_deposit_amount(self):
    plan = self.financing_plan
    bill = self.amount
    rec = self.recurring_model
    due = getdate(self.due_date)
    today = getdate()

    if plan == "Once":
        self.deposit_amount = bill
        frappe.msgprint(f"Amount to be paid: {self.deposit_amount}, due in 1 day (Once).")
        
    elif plan == "Daily":
        num_days = max((due - today).days, 1)  # Ensure at least 1 day for division
        self.deposit_amount = bill / num_days
        frappe.msgprint(f"Amount to be paid: {self.deposit_amount:.2f}, over {num_days} days.")

    elif plan == "Weekly":
        num_days = max((due - today).days, 1)
        num_weeks = num_days / 7.0  # Allow fractional weeks
        self.deposit_amount = bill / num_weeks
        frappe.msgprint(f"Amount to be paid: {self.deposit_amount:.2f}, over {num_weeks:.2f} weeks ({num_days} days).")

    elif plan == "Monthly":
        num_days = max((due - today).days, 1)
        num_months = num_days / 30.0  # Allow fractional months
        self.deposit_amount = bill / num_months
        frappe.msgprint(f"Amount to be paid: {self.deposit_amount:.2f}, over {num_months:.2f} months ({num_days} days).")
