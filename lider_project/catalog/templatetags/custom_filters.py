from django import template

register = template.Library()  # Обязательная строка!

@register.filter(name='get_attribute_values')  # Явное указание имени
def filter_attributes(attribute_values, attribute):
    """Фильтрует значения атрибутов для конкретного атрибута"""
    return [
        av.value
        for av in attribute_values
        if av.attribute.id == attribute.id and av.value
    ]