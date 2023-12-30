from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def paginate_url(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)
    if urlencode:
        querystring = urlencode.split("&")
        filter_querystring = filter(lambda p: p.split("=")[0] != field_name, querystring)
        encoded_querystring = "&".join(filter_querystring)
        url = "{}&{}".format(url, encoded_querystring)
        print(url)
    return url


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=2, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number,
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)


@register.filter
def get_all_fields(obj):
    return obj._meta.fields


@register.filter
def get_all_field_values(obj):
    return [getattr(obj, field.name) for field in obj._meta.fields]


@register.filter
def zip_fields_values(fields, values):
    return zip(fields, values)


@register.filter
def render_form_with_instance(form, instance):
    for field in form:
        if field.name != "user":
            field.field.widget.attrs['value'] = getattr(instance, field.name)
    return form


