# Copyright (c) 2024, satish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):
	def validate(self):
		self.check_duplicates()
		self.assign_random_seat()
		

	def before_save(self):
		total_amount = 0
		add_on = self.add_on
		for item in self.add_on:
			total_amount += item.amount
		self.total_amount = total_amount + self.flight_price

		self.check_capacity()


	def check_duplicates(self):
		items = set()
		unique_items = []
		for item in self.add_on:
			if item.item not in items:
				items.add(item.item)
				unique_items.append(item)
		self.add_on = unique_items


	def assign_random_seat(self):
		alpha = ['A','B','C','D','E']
		if not self.seat:
			self.seat = f"{random.randint(00,99)}{random.choice(alpha)}"

	# def on_submit(self):
	# 	doc = frappe.get_doc("Airplane Flight",self.flight)
	# 	doc.db_set('status','Completed')
	# 	doc.save()

	def check_capacity(self):
		flight_id = self.flight
		flight = frappe.get_doc('Airplane Flight', flight_id)
		airplane_id = flight.airplane
		airplane = frappe.get_doc('Airplane', airplane_id)
		capacity = airplane.capacity
		ticket_count = frappe.db.count('Airplane Ticket', {'flight': flight_id})

		if ticket_count >= capacity:
			frappe.throw(f'The number of tickets for this flight exceeds the capacity of {capacity} seats for the airplane.')
		

def check_status_before_submit(doc, method):
	if doc.status != "Boarded" :
		frappe.throw(("Cannot submit application unless Ticket is Status is Boarded"))

		
