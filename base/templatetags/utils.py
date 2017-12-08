"""
Utils template tags
"""

from django import template

register = template.Library()
@register.filter
def group(array, group_length):
    return zip(*(iter(array),) * group_length)
