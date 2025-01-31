# Copyright (c) 2025, Bhavya and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# Script Report Logic
# import frappe
# from frappe.utils import nowdate, add_days

# def execute(filters=None):
#     today = nowdate()
#     next_week = add_days(today, 7)

#     columns = [
#         {"fieldname": "name", "label": "Event ID", "fieldtype": "Link", "options": "Event Details", "width": 150},
#         # {"fieldname": "title", "label": "Title", "fieldtype": "Data", "width": 200},
#         {"fieldname": "start_date", "label": "Start Date", "fieldtype": "Date", "width": 120},
#         {"fieldname": "end_date", "label": "End Date", "fieldtype": "Date", "width": 120},
#     ]

#     data = frappe.get_all(
#         "Event Details",
#         filters={"start_date": ["between", [today, next_week]]},
#         fields=["name","start_date", "end_date"],
#     )
    
	
#     return columns, data
import frappe
from frappe.utils import nowdate, add_days

def execute(filters=None):
    today = nowdate()
    next_week = add_days(today, 7)

    
    columns = [
        {"fieldname": "name", "label": "Event ID", "fieldtype": "Link", "options": "Event Details", "width": 150},
        {"fieldname": "start_date", "label": "Start Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "end_date", "label": "End Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "event_count", "label": "Events Count", "fieldtype": "Int", "width": 120},
    ]

   
    events = frappe.get_all(
        "Event Details",
        filters={"start_date": ["between", [today, next_week]]},
        fields=["name", "start_date", "end_date"],
    )

   
    data = []
    for event in events:
        start_date = event.get("start_date")
        end_date = event.get("end_date")
        
       
        overlapping_events = frappe.get_all(
            "Event Details",
            filters={
                "start_date": ["<=", end_date],
                "end_date": [">=", start_date],
                "name": ["!=", event["name"]],  
            },
            fields=["name"],
        )
        
       
        event["event_count"] = len(overlapping_events)
        data.append(event)

    return columns, data

