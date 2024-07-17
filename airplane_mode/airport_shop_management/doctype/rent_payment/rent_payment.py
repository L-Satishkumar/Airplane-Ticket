# Copyright (c) 2024, satish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
from frappe import utils
from airplane_mode.task import send_rent_reminders

class RentPayment(Document):
	def validate(self):
		self.generate_receipt()
		self.default_rent_payment()
		send_rent_reminders()

	def before_save(self):
		if not self.receipt:
			self.receipt = f"{self.tenant}-{utils.today()}-{random.randint(00,99)}"

	
	def default_rent_payment(self):
		if not self.rent_amount:
			global_config = frappe.get_single('Shop Settings')
			self.rent_amount = global_config.default_rent_amount

	def generate_receipt(self):
		if self.paid == 1:
			doc = frappe.new_doc('Receipt')
			doc.receipt_number = self.receipt
			doc.shop = self.shop
			doc.tenant = self.tenant
			doc.rent_amount = self.rent_amount
			doc.payment_date = self.payment_date
			doc.due_date = self.due_date
			doc.insert()
			doc.save()

	