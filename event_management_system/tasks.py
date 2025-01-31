import frappe
from frappe.email.queue import flush
from frappe.utils import getdate, add_days

def send_event_notifications():
    """Scheduled job to send event notifications to all participants."""

    
    event_details = frappe.get_all(
        "Event Details",
        fields=["name", "event", "start_date"]
    )

    if not event_details:
        frappe.logger().info("No events found.")
        return

    for event in event_details:
        
        event_start_date = getdate(event.start_date)

       
        day_before_event = add_days(event_start_date, -1)

        
        if getdate() == day_before_event:
            
            participants = frappe.get_all(
                "Participants",
                filters={"parent": event.name},
                fields=["email"]
            )

            if not participants:
                frappe.logger().warning(f"No participants found for event {event.event}")
                continue

            for participant in participants:
                if not participant.email:
                    frappe.logger().warning(f"No email found for participant in event {event.event}")
                    continue 

                subject = f"Notification for Event: {event.event}"
                message = f"""
<p>Dear Participant,</p>
<p>This is a reminder for the event: <b>{event.event}</b> happening tomorrow.</p>
<p>We hope to see you there!</p>
<br>
<p>Regards,<br>Event Management Team</p>
                """

                try:
                    
                    frappe.sendmail(
                        recipients=participant.email,
                        subject=subject,
                        message=message
                    )
                    frappe.logger().info(f"Email queued for {participant.email} regarding {event.event}")

                   
                    frappe.db.set_value("Event Details", event.name, "email_sent", 1)

                except Exception as e:
                    frappe.log_error(f"Error sending email to {participant.email}: {str(e)}")
                    frappe.logger().error(f"Failed to queue email for {event.event}: {str(e)}")

    
    frappe.enqueue(method=flush, queue="short")
    frappe.logger().info("Email queue flushed and emails sent.")

    frappe.db.commit()


