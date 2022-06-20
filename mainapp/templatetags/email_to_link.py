from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def email_to_link(e_str):
    return mark_safe(f'<a href="mailto:{e_str}">{e_str}</a>')
