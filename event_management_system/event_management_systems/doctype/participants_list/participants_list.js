frappe.ui.form.on('Participants List', {
    refresh: function(frm) {
        
        const participantName = frm.doc.participant_name;

        if (participantName) {
            
            frappe.call({
                method: "event_management_system.event_management_systems.doctype.participants_list.participants_list.check_event_end_date",  // Replace with your actual server script method path
                args: {
                    participant_name: participantName
                },
                callback: function(response) {
                    const result = response.message;

                   
                    if (result.status === "success") {
                       
                        frm.add_custom_button(__('Download Event Certificate'), function() {
                            
                            const participantName = frm.doc.participant_name;  
                            const event = frm.doc.event; 

                            
                            if (!participantName || !event) {
                                frappe.msgprint("Please ensure both participant name and event are entered.");
                                return;
                            }

                            
                            const printFormat = "Event Certificate";  

                            
                            const url = `/api/method/frappe.utils.print_format.download_pdf?doctype=Participants%20List&name=${encodeURIComponent(frm.doc.name)}&format=${encodeURIComponent(printFormat)}&no_letterhead=0`;

                            
                            window.open(url, '_blank');
                        });
                    } else {
                        
                        frm.clear_custom_buttons();
                        frappe.msgprint(result.message);
                    }
                }
            });
        } else {
           
            frappe.msgprint("Participant name is missing.");
        }
    }
});


frappe.ui.form.on('Participants List', {
    refresh: function(frm) {
        update_alert_field(frm);
    },
    end_date: function(frm) {
        update_alert_field(frm);
    }
});

function update_alert_field(frm) {
    if (frm.doc.end_date) {
        let today = frappe.datetime.get_today();
        let days_before_value = frappe.datetime.get_day_diff(frm.doc.end_date, today); 

        frm.set_value('days_before', days_before_value);
    }
}

frappe.ui.form.on('Participants List', {
    refresh: function(frm) {
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'User',
                filters: { name: frappe.session.user },
                fieldname: ['full_name', 'email']
            },
            callback: function(response) {
                if (response.message) {
                 
                    frm.set_value('participant_name', response.message.full_name);
                   
                    frm.set_value('email', response.message.email);
                }
            }
        });
    }
});


frappe.ui.form.on("Participants", {
    refresh: function(frm) {
        
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Event Details",
                    name: frm.doc.event,
                },
                callback: function(r) {
                    if (r.message) {
                        let capacity = r.message.capacity;
                        frappe.msgprint(capacity)
                        
                    }
                }
            });
        
    }
});



frappe.ui.form.on('Participants List', {
    validate: function (frm) {
      
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Event Details', 
                filters: {
                    name: frm.doc.event, 
                },
                fieldname: 'capacity',
            },
            callback: function (r) {
                if (r.message) {
                    let capacity = r.message.capacity;

                   
                    frappe.call({
                        method: 'frappe.client.get_list',
                        args: {
                            doctype: 'Participants List', 
                            filters: {
                                event: frm.doc.event, 
                            },
                            fields: ['name'], 
                        },
                        callback: function (res) {
                            let participant_count = res.message.length; 

                            if (participant_count >= capacity) {
                                frappe.msgprint({
                                    title: __('Capacity Reached'),
                                    message: __('This event already has the maximum number of participants.'),
                                    indicator: 'red',
                                });

                                frappe.validated = false; 
                            }
                        },
                    });
                } else {
                    frappe.msgprint(__('Unable to fetch capacity for the selected event.'));
                }
            },
        });
    },
});


