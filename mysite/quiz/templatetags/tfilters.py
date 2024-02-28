from django import template

register = template.Library()

@register.filter
def return_index(list, i):
    try:
        return list[i]
    except:
        return None
                            