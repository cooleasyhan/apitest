import json

from django import template
from django.template.defaultfilters import stringfilter
from pprint import pformat
register = template.Library()

@register.filter
def json_format(value):
    try:
        obj = json.loads(value)
        return json.dumps(obj, indent=4)
    except Exception as e:
        return value

@register.filter
def dict_format(value):
    if not isinstance(value, dict):
        return value
    
    return pformat(value)

