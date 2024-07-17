# Copyright (c) 2024, satish and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [
		{
			"label":"Airline",
			"fieldname":"airline",
			"fieldtype":"Link",
			"options":"Airline",
			"width": 200
		},
		{

			"label":"Revenue",
			"fieldname":"revenue",
			"fieldtype":"Currency",
			"width": 200,
		}
	], []

	data = frappe.db.sql("""
        SELECT 
            air.name AS airline,
            COALESCE(SUM(tic.total_amount), 0) AS revenue
        FROM
            `tabAirplane Ticket` tic
        RIGHT JOIN
			`tabAirplane Flight` fli ON tic.flight = fli.name
		RIGHT JOIN
			`tabAirplane` pla ON fli.airplane = pla.name
		RIGHT JOIN
			`tabAirline` air ON pla.airline = air.name
		GROUP BY
			air.name
    """, as_dict=True)
	
	total_revenue = 0
	for revenue in data:
		total_revenue += revenue.get('revenue')

	chart = {
		"data": {
			"labels": [d.airline for d in data],
			"datasets": [{
				"name": "Revenue by month",
				"values": [d.revenue for d in data],
			}]
		},
		"type": "donut",
	}

	report_summary = [{
		"label": "Total Revenue",
        "value": total_revenue,
        "datatype": "Currency",
        "indicator": "Green" if total_revenue > 0 else "Red",
        "currency": "INR"
    }]

	return columns, data ,None, chart, report_summary