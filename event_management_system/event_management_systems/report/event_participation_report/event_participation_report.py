# # Copyright (c) 2025, Bhavya and contributors
# # For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns() 
    data = get_data(filters)  
    
   
    return columns, data  

def get_columns():
    return [
        
        {
            "fieldname": "participant_name",
            "fieldtype": "Link",
            "label": "Participant Name",
            "options":"Participants List",
            "width": 200,
        },
        {
            "fieldname": "enrollment_number",
            "fieldtype": "Data",
            "label": "Enrollment Number",
            "width": 200,
        },
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
            "width": 200,
        },
    ]

def get_data(filters):
    
    event_filters = {}
    if filters and filters.get("event_details"):
        event_filters = {"event": filters["event_details"]}

    event_details = frappe.get_all(
        "Event Details",
        filters=event_filters,
        fields=["name", "start_date", "event"],
    )
    
    if not event_details:
       
        return []

    data = []
    for event in event_details:
        event_name = event.get('event')
        start_date = event.get('start_date')

        
        participants = frappe.get_all(
            "Participants", 
            filters={"parent": event["name"]},
            fields=["participant_name", "enrollment_number"]
        )
        
        for participant in participants:
            participant_name = participant.get('participant_name')
            enrollment_number = participant.get('enrollment_number')

            
            data.append([
                participant_name,
                enrollment_number,
                event_name,
                start_date,
            ])
    
    return data



# import frappe

# def execute(filters=None):
#     columns = get_columns() 
#     data = get_data()  
    
    
#     frappe.msgprint("Displaying empty columns") 
#     return columns, data  

# def get_columns():
#     return [
#         {
#             "fieldname": "participant_name",
#             "fieldtype": "Link",
#             "label": "Participant Name",
#             "width": 200,
#         },
#         {
#             "fieldname": "enrollment_number",
#             "fieldtype": "Data",
#             "label": "Enrollment Number",
#             "width": 200,
#         },

#         {
#             "fieldname": "event",
#             "fieldtype": "Data",
#             "label": "Event",
#             "width": 200,
#         },
#         {
#             "fieldname": "start_date",
#             "fieldtype": "Date",
#             "label": "Start Date",
#             "width": 200,
#         },
#     ]

# def get_data():
#     event_details = frappe.get_all(
#         "Event Details",
#         fields=["start_date", "event"],
#     )

#     participants = frappe.get_all(
#         "Participants",
#         filters={"parent": event["name"]},
#         fields=["participant_name", "enrollment_number"],
#     )
    
#     data = []
#     for i in event_details:
#         event = i.get('event') 
#         start_date = i.get('start_date') 

#     for j in  participants:
#         participant_name = j.get('participant_name')
#         enrollment_number = j.get('enrollment_number')


    
       
#         data.append([event, start_date,participant_name,enrollment_number])
    
#     return data
