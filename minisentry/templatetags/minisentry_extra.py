import datetime
from pprint import pformat, pprint

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def iso_to_date(value: str):
    """
    convert iso formatted time string, assume UTC if no TZ info present.

    >>> iso_to_date('2023-08-06T11:03:25.198625Z')
    datetime.datetime(2023, 8, 6, 11, 3, 25, 198625, tzinfo=datetime.timezone.utc)
    >>> iso_to_date('2023-08-06T11:03:25.198625')
    datetime.datetime(2023, 8, 6, 11, 3, 25, 198625)
    """
    ret = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if not ret.tzinfo:
        ret.replace(tzinfo=datetime.timezone.utc)
    return ret


@register.filter
def stringify2(value: dict):
    """
    TODO: this is a plaster, code sth proper
    if var value is a dict, pprint it
    """
    if not value:
        return ()
    ret = []
    for var_name, var_value in value.items():
        if isinstance(var_value, (dict, list)):
            var_value = pformat(value, indent=4, width=120)
            var_value = mark_safe(f"<details><summary>show</summary>{var_value}</details>")
        ret.append((var_name, var_value))
    return ret
