# Copyright (c) 2025, Bhavya and contributors
# For license information, please see license.txt


 

import frappe
from frappe.model.document import Document

import frappe
from frappe.utils import today, add_days, getdate


 
class EventDetails(Document):
    pass  

 
def update_event_status(doc, method):

    if doc.registered_participants >= doc.capacity:

        doc.status = "Full"

    elif doc.registered_participants < doc.capacity:

        doc.status = "Available"

    else:

        doc.status = "Overbooked"

    

    doc.set("status", doc.status)

    doc.db_update()

 








