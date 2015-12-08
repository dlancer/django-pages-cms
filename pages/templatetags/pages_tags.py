from django import template
from django.template import Context, Template
from django.utils.html import escape

from pages.conf import settings


register = template.Library()


@register.assignment_tag()
def get_page_object(objects, sid):
    """
    **Arguments**

    ``objects``
        all objects

    ``sid`
        symbolic id for object selection

    :return selected object
    """
    selected_object = None

    for obj in objects:
        if obj.sid == sid:
            selected_object = obj
            break
    return selected_object


@register.assignment_tag(takes_context=True)
def get_page_object_by_name(context, name):
    """
    **Arguments**

    ``name`
        name for object selection

    :return selected object
    """
    selected_object = None

    try:
        for obj_type in context['page']['content']:
            for obj in context['page']['content'][obj_type]:
                if obj.name == name:
                    selected_object = obj
                    break
        if selected_object is None:
            for obj_type in context['page']['content']:
                for obj in context['page']['ext_content'][obj_type]:
                    if obj.name == name:
                        selected_object = obj
                        break
    except TypeError:
        pass
    return selected_object


@register.assignment_tag(takes_context=True)
def get_page_object_by_id(context, object_type, oid):
    """
    **Arguments**

    ``object_type``
        object type

    ``oid``
        id for object selection

    :return selected object
    """
    if type(oid) != int:
        raise template.TemplateSyntaxError('page_object_by_id tag requires a integer argument')

    selected_object = None

    try:
        try:
            for obj in context['page']['content'][object_type]:
                sid = '{0:>s}:{1:>s}:{2:>s}:{3:>d}'.format(
                    obj.language, context['page']['page'].name, obj.type, oid
                )
                if obj.sid == sid:
                    selected_object = obj
                    break
        except TypeError:
            pass
    except KeyError:
        try:
            try:
                for obj in context['page']['ext_content'][object_type]:
                    sid = '{0:>s}:{1:>s}:{2:>s}:{3:>d}'.format(
                        obj.language, context['page']['page'].name, obj.type, oid
                    )
                    if obj.sid == sid:
                        selected_object = obj
                        break
            except TypeError:
                pass
        except KeyError:
            raise template.TemplateSyntaxError('wrong content type: {0:>s}'.format(object_type))
    return selected_object


@register.assignment_tag(takes_context=True)
def get_page_objects_by_type(context, object_type):
    """
    **Arguments**

    ``object_type``
        object type

    :return selected objects
    """
    try:
        objects = context['page']['content'][object_type]
    except KeyError:
        raise template.TemplateSyntaxError('wrong content type: {0:>s}'.format(object_type))
    return objects


@register.assignment_tag(takes_context=True)
def get_page_objects_by_ext_type(context, object_type):
    """
    **Arguments**

    ``object_type``
        object type

    :return selected objects
    """
    try:
        objects = context['page']['ext_content'][object_type]
    except KeyError:
        raise template.TemplateSyntaxError('wrong content type: {0:>s}'.format(object_type))
    return objects


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


@register.simple_tag(takes_context=True)
def get_page_active_css_class(context, name):
    css_class = ''
    try:
        if context['page']['page'].name == name:
            css_class = settings.PAGES_PAGE_ACTIVE_CSS_CLASS
    except KeyError:
        pass
    return css_class
