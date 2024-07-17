import frappe

def get_context(context):
    # Fetch shops that are not occupied
    shops = frappe.get_all('Shop', filters={'occupied': 0}, fields=['shop_name', 'shop_number', 'shop_location', 'airport', 'tenant_name', 'tenant_email'])
    
    # Debugging: Print the fetched shops to the console
    frappe.log_error(message=shops, title="Fetched Shops")
    
    # Pass the shops data to the context
    context.shops = shops
