
from django import template
from users.models import User
register = template.Library()

@register.filter(name='filter_by_category')
def filter_by_category_name(value, ordering):
    result = filter(lambda x:x if x['category__name'] == ordering else None, value)
    return result