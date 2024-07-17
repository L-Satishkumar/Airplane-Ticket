import frappe
from frappe.utils import today, add_days, formatdate, getdate
from frappe.core.doctype.communication.email import make

def send_rent_reminders():
    settings = frappe.get_single("Shop Settings")
    if not settings.rent_reminders:
        return

    tomorrow = getdate(add_days(today(), 1))
    
    tenants = frappe.get_all('Tenant', fields=['name', 'email'])
    for tenant in tenants:
        rent_payments = frappe.get_all('Rent Payment', filters={'tenant': tenant.name}, fields=['payment_date', 'shop', 'rent_amount', 'due_date'])
        
        for rent_payment in rent_payments:
            if getdate(rent_payment.due_date) == tomorrow:
                shop_name = frappe.db.get_value('Shop', rent_payment.shop, 'shop_name')
                
                subject = f"Rent Due Reminder for Shop {shop_name}"
                message = f"""
                    Dear {tenant.name},
                    
                    This is a friendly reminder that the rent for shop {shop_name} amounting to {rent_payment.rent_amount} is due on {formatdate(rent_payment.due_date)}.
                    
                    Please ensure that the payment is made by the due date to avoid any late fees.
                    
                    Thank you.
                    
                    Regards,
                    Airport Management
                """
                
                make(
                    recipients=[tenant.email],
                    subject=subject,
                    content=message,
                    send_email=True
                )
