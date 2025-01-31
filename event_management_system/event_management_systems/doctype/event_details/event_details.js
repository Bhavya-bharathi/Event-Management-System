// Copyright (c) 2025, Bhavya and contributors
// For license information, please see license.txt



frappe.ui.form.on('Event Details', {
    refresh: function (frm) {
       
        let capacity = frm.doc.capacity;

        
        if (!capacity || capacity <= 0) {
            frappe.msgprint(__('Please enter a valid Capacity value.'));
            return;
        }

       
        let child_table = frm.doc.participants || [];

        
        if (child_table.length < capacity) {
            let rows_to_add = capacity - child_table.length;

            for (let i = 0; i < rows_to_add; i++) {
                frm.add_child('participants');
            }

            frappe.msgprint(__('Added missing rows to match the Capacity.'));
        } 
        
        else if (child_table.length > capacity) {
            let rows_to_remove = child_table.length - capacity;

            for (let i = 0; i < rows_to_remove; i++) {
                frm.doc.participants.pop();
            }

            frappe.msgprint(__('Removed extra rows to match the Capacity.'));
        }

       
        frm.refresh_field('participants');
    }
});



frappe.ui.form.on('Event Details', {
    refresh: function (frm) {
        
        update_row_count(frm);
    },
    validate: function (frm) {
        
        update_row_count(frm);
    },
    participants_on_form_rendered: function (frm) {
        
        update_row_count(frm);
    }
});


function update_row_count(frm) {
    
    if (frm.doc.participants) {
       
        const rowCount = frm.doc.participants.length;

        
        frm.set_value('registered_participants', rowCount); 
    } else {
       
        frm.set_value('registered_participants', 0); 
    }
}
