import frappe

def get_context(context):
    
    color = frappe.form_dict.get('color', 'black')
    
    context.color = color
    return context
