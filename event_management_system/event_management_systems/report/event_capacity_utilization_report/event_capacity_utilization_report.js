// Copyright (c) 2025, Bhavya and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Event Capacity Utilization Report"] = {
	"filters": [{
		"fieldname": "event_details",
		"label": "Event",
		"fieldtype": "Link",
		"options": "Event Details",
		"reqd": 1

	}

	]
};
