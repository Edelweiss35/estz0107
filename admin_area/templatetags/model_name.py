from django import template
register = template.Library()
from django.utils import formats, dateparse

from django.db.models import fields
from django.db.models.fields import files

from django.utils.safestring import mark_safe

# @register.simple_tag
# def model_name(value):
#     '''
#     Django template filter which returns the verbose name of a model.
#     '''
#     if hasattr(value, 'model'):
#         value = value.model
#         return value._meta.verbose_name.title()
#
# @register.simple_tag
# def model_name_plural(value):
#     '''
#     Django template filter which returns the plural verbose name of a model.
#     '''
#     if hasattr(value, 'model'):
#         value = value.model
#         return value._meta.verbose_name_plural.title()

@register.simple_tag
def field_name(value, field):
    '''
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    '''
    field = field.split('__', 1)[0]  # remove related
    if hasattr(value._meta.get_field(field), 'verbose_name'):
        return value._meta.get_field(field).verbose_name
    else:
        return field


@register.simple_tag
def convert_fields_value_nice_display(model, field, value):
    # try to show foreng title
    # try:
    #     return value.status.title
    # except:
    #     pass

    if "__" in field:
        return value

    if hasattr(model._meta.get_field(field), 'choices') and model._meta.get_field(field).choices:
        a = model._meta.get_field(field).choices
        display = [item for item in a if item[0] == value]
        to_return = value
        if display:
            to_return = display[0][1]
        return to_return
    elif type(model._meta.get_field(field)) == fields.DateTimeField:
        return formats.date_format(value, "SHORT_DATETIME_FORMAT")
    elif type(model._meta.get_field(field)) == files.FileField:
        if value.name:
            return mark_safe('<div>Вложение: <a href="{}" target="_blank">Открыть</a> /'
                             ' <a href="{}" download>Скачать</a></div>'
                             .format(value.url, value.url))

            # return mark_safe('<a target="blank" href="{}">Вложение</a>'.format(value.url))
        else:
            return value
    else:
        return value



