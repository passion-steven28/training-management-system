# dashboard/templatetags/dashboard_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the arg and value"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def subtract(value, arg):
    """Subtract arg from value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0