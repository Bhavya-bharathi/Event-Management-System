import frappe
from frappe.utils import getdate, nowdate

def send_certificate_email():
    
    participants = frappe.get_all('Participants List', 
                                  filters={'email': ['is', 'set']}, 
                                  fields=['name', 'participant_name', 'email', 'end_date'])

 
    for participant in participants:
        try:
           
            if getdate(participant['end_date']) >= getdate(nowdate()):
                send_email_to_participant(participant)
        except Exception as e:
            
            frappe.log_error(f"Error sending email to {participant['email']}: {str(e)}", "send_certificate_email")

def send_email_to_participant(participant):
    try:
        
        frappe.sendmail(
            recipients=participant['email'],
            subject="Certificate for Event Participation",
            message=f"Dear {participant['participant_name']},<br><br>Congratulations on your participation! Your certificate will be available soon."
        )
        frappe.msgprint(f"Certificate email sent to {participant['email']}")

    except Exception as e:
       
        frappe.log_error(f"Error sending certificate to {participant['email']}: {str(e)}", "send_certificate_email")

