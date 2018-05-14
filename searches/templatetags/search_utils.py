from django import template


register = template.Library()


@register.filter
def get_from_key(dic, key):
    """
    Returns the value of the dict for the key.
    This is necessary when the key starts with a '_', because django templates
    doesn't allow to access such keys (eg: object._source)
    """
    return dic.get(key)
