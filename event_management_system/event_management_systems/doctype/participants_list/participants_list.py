import frappe
from frappe.model.document import Document
 
class ParticipantsList(Document):
    pass
 
@frappe.whitelist()
def check_event_end_date(participant_name):
    participant = frappe.get_all('Participants List', filters={'participant_name': participant_name}, limit=1)
 
    if participant:
        participant_doc = frappe.get_doc('Participants List', participant[0].name)
 
        event_end_date = participant_doc.end_date
        today = frappe.utils.today()
 
       
        if event_end_date:
            if event_end_date >= today:
                return {"message": "Event End Date is today or in the future", "status": "success"}
            else:
                return {"message": "Event End Date is in the past", "status": "error"}
        else:
            return {"message": "Event End Date is not set", "status": "error"}
    else:
        return {"message": "Participant not found", "status": "error"}



