# Copyright (c) 2024, satish and contributors
# For license information, please see license.txt

import frappe
# from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
    def before_submit(self):
        self.status = "Completed"

    def validate(self):
        self.check_gate()

    def check_gate(self):
        existing_gate = frappe.db.exists('Airplane Flight',{"gate_number": self.gate_number})
        if self.gate_number == existing_gate:
            frappe.throw(f'The gate number {self.gate_number} is already assigned to another flight')

    def on_update(self):
        if self.is_new() or not self.get_doc_before_save():
            return

        old_doc = self.get_doc_before_save()
        if old_doc.gate_number != self.gate_number:
            self.update_ticket_gate_numbers()

    def update_ticket_gate_numbers(self):
        tickets = frappe.get_all('Airplane Ticket', filters={'flight': self.name}, fields=['name'])
        for ticket in tickets:
            ticket_doc = frappe.get_doc('Airplane Ticket', ticket.name)
            ticket_doc.gate_number = self.gate_number
            ticket_doc.save()

        frappe.msgprint("Gate number for all tickets updated to {}".format(self.gate_number))

        notify_passengers_about_gate_change(self.name, self.gate_number)

def notify_passengers_about_gate_change(flight_name, new_gate_number):
    tickets = frappe.get_all('Airplane Ticket', filters={'flight': flight_name}, fields=['name', 'email'])
    for ticket in tickets:
        subject = "Gate Number Changed for Your Flight"
        message = f"Dear Passenger,\n\nThe gate number for your flight {flight_name} has been changed to {new_gate_number}. Please check your ticket for the updated gate number.\n\nThank you."
        
        frappe.sendmail(
            recipients=[ticket.email],
            subject=subject,
            message=message
        )

        