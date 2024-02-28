from django import template

register = template.Library()
#Author: Tom

#Custom template filter for accessing array indexes.
@register.filter
def return_index(list, i):
    try:
        return list[i]
    except:
        return None
                            