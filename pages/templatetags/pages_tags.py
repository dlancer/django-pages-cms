from django import template
from django.template import Context, Template
from django.utils.html import escape

from pages.conf import settings


register = template.Library()


@register.assignment_tag()
def get_page_object(objects, name):
    """
    **Arguments**

    ``objects``
        all objects

    **Keyword arguments**

    ``name``
        name for object selection

    :return selected object
    """
    selected_object = None

    for obj in objects:
        if obj.name == name:
            selected_object = obj
            break
    return selected_object


@register.assignment_tag(takes_context=True)
def get_page_object_by_id(context, object_type, oid):
    """
    **Arguments**

    ``object_type``
        object type

    **Keyword arguments**

    ``oid``
        id for object selection

    :return selected object
    """
    if type(oid) != int:
        raise template.TemplateSyntaxError('page_object_by_id tag requires a integer argument')

    selected_object = None

    try:
        for obj in context['page']['content'][object_type]:
            name = '{0:>s}:{1:>s}:{2:>s}:{3:>d}'.format(
                obj.language, obj.type, context['page']['page'].name, oid
            )
            if obj.name == name:
                selected_object = obj
                break
        if selected_object is None:
            for obj in context['page']['ext_content'][object_type]:
                name = '{0:>s}:{1:>s}:{2:>s}:{3:>d}'.format(
                    obj.language, obj.type, context['page']['page'].name, oid
                )
                if obj.name == name:
                    selected_object = obj
                    break
    except KeyError:
        raise template.TemplateSyntaxError('wrong content type: {0:>s}'.format(object_type))
    return selected_object


@register.simple_tag(takes_context=True)
def page_text_by_id(context, oid):
    obj = get_page_object_by_id(context, 'text', oid)
    if obj is None:
        return None
    if obj.is_template and settings.PAGES_ALLOW_DJANGO_TEMPLATES:
        tpl = Template(obj.text)
        text = tpl.render(Context(context))
    else:
        text = escape(obj.text)
    return text


@register.assignment_tag(takes_context=True)
def get_page_text_by_id(context, oid):
    return page_text_by_id(context, oid)


@register.assignment_tag(takes_context=True)
def get_raw_page_text_by_id(context, oid):
    obj = get_page_object_by_id(context, 'text', oid)
    return obj.text if obj else None


@register.simple_tag(takes_context=True)
def page_markdown_by_id(context, oid):
    obj = get_page_object_by_id(context, 'markdown', oid)
    if obj is None:
        return None
    return obj.text


@register.assignment_tag(takes_context=True)
def get_page_markdown_by_id(context, oid):
    return page_markdown_by_id(context, oid)


@register.assignment_tag(takes_context=True)
def get_page_image_by_id(context, oid):
    obj = get_page_object_by_id(context, 'image', oid)
    return obj if obj else None
