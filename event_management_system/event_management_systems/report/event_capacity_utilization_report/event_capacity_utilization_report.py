# Copyright (c) 2025, Bhavya and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "event",
            "fieldtype": "Data",
            "label": "Event",
            "width": 200,
        },
        {
            "fieldname": "start_date",
            "fieldtype": "Date",
            "label": "Start Date", 
        },
        {
            "fieldname": "capacity",
            "fieldtype": "Int",
            "label": "Maximum Capacity", 
        },
        {
            "fieldname": "participant_name",
            "fieldtype": "Data",  
            "label": "Participant Name",
        },
        {
            "fieldname": "enrollment_number",
            "fieldtype": "Data",
            "label": "Enrollment Number",
        },
        {
            "fieldname": "registered_participants",
            "fieldtype": "Data",
            "label": "Registered Participants",
        },

    ]

def get_data(filters):
    
    event_filters = {}
    if filters and filters.get("event_details"):
        event_filters = {"event": filters["event_details"]}

    event_details = frappe.get_all(
        "Event Details",
        filters=event_filters,
        fields=["name", "start_date", "event", "capacity","registered_participants"],
    )
    
    if not event_details:
        return [] 

    data = []
    for event in event_details:
        event_name = event.get('event')
        start_date = event.get('start_date')
        capacity = event.get('capacity')
        registered_participants=event.get('registered_participants')

       
        participants = frappe.get_all(
            "Participants", 
            filters={"parent": event["name"]},
            fields=["participant_name", "enrollment_number"]
        )
        
        for participant in participants:
            participant_name = participant.get('participant_name')
            enrollment_number = participant.get('enrollment_number')

        

           
            data.append({
                "event": event_name,
                "start_date": start_date,
                "capacity": capacity,
                "participant_name": participant_name,
                "enrollment_number": enrollment_number,
                "registered_participants": registered_participants,
            })
    
    return data





