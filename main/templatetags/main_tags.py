from django import template

register = template.Library()


@register.filter
def get(container, key):
    """http://stackoverflow.com/a/20523607/2202986"""
    if type(container) is dict:
        return container.get(key)
    elif type(container) in (list, tuple):
        return container[key] if len(container) > key else None
    return None