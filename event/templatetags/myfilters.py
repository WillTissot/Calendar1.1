from django import template


register = template.Library()

@register.filter
def filter_changes(event):
    return event.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()