from django import template

from pages.templatetags.pages_tags import get_page_object_by_id

register = template.Library()


@register.simple_tag(takes_context=True)
def page_video_by_id(context, oid):
    obj = get_page_object_by_id(context, 'video', oid)
    if obj is None:
        return None
    return obj


@register.assignment_tag(takes_context=True)
def get_page_video_by_id(context, oid):
    return page_video_by_id(context, oid)
