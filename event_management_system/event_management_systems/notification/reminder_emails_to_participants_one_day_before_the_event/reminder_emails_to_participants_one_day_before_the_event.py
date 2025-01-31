


import frappe

def send_notification_email():
    recipient_email = "bhavya2akkala@gmail.com"  
    subject = "Subject of the Email"
    message = "This is the content of the email message."

    frappe.sendmail(
        recipients=recipient_email,
        subject=subject,
        message=message
    )


send_notification_email()


