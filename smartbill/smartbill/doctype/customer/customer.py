# Copyright (c) 2024, Gatura Njenga and contributors
# For license information, please see license.txt

import frappe
import re
from datetime import date, datetime, timedelta
from frappe.model.document import Document

class Customer(Document):
        def before_save(self):
                set_full_name(self)
        
        def validate(self):
                valid_email(self)
                validate_date_of_birth(self)
                set_age(self)
                validate_age(self)
        
        
# set full_name
def set_full_name(self):
        first_name = self.first_name.strip().title()
        middle_name = self.middle_name_optional.strip().title() if self.middle_name_optional else ""
        last_name = self.last_name.strip().title()
        
        # set all names to be title 
        self.first_name = first_name
        self.middle_name_optional = middle_name if self.middle_name_optional else ""
        self.last_name = last_name
        
        # if middle_name is provided include it in full_name
        if middle_name:
                self.full_name = f"{first_name} {middle_name} {last_name}"
        else:
                self.full_name = f"{first_name} {last_name}"
                

# valid email? should contain @ and . after @
def valid_email(self):
        pattern = "[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]"
        e = self.email
        if re.search(pattern, e):
                return True
        else:
                frappe.throw("Invalid email address")
                # return False
                

# validate date_of_birth
def validate_date_of_birth(self):
        if self.date_of_birth > frappe.utils.nowdate():
                frappe.throw("Date of birth cannot be in the future")
                

# calculate age
def set_age(self):
    today = date.today()

    # Convert the date_of_birth from string to date object with format 'YYYY-MM-DD'
    dob = datetime.strptime(self.date_of_birth, '%Y-%m-%d').date()

    age_years = today.year - dob.year
    age_months = today.month - dob.month
    age_days = today.day - dob.day

    if age_months < 0 or (age_months == 0 and age_days < 0):
        age_years -= 1
        age_months += 12

    if age_days < 0:
        # Adjust day difference
        previous_month_last_day = (today.replace(day=1) - timedelta(days=1)).day
        age_days += previous_month_last_day
        age_months -= 1

    self.age = f"{age_years} years {age_months} months {age_days} days"
    
    
# validate age > 18
def validate_age(self):
    if self.age:
        # Extract the number of years from the age string
        age_years = int(self.age.split()[0])

        if age_years < 18:
            frappe.throw("Must be 18 or older")
            

