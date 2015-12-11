"""Implements admin interface for Pages"""

import importlib

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from mptt.admin import MPTTModelAdmin
from guardian.admin import GuardedModelAdmin

from pages.conf import settings
from pages.models import Page
from pages.models import PageContent
from pages.models import PageContentType
from pages.admin import pagecontenttypes
from pages.admin.pagecontent import PageContentInline


PAGE_EXT_CONTENT_INLINES = []

if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
    if settings.PAGES_PAGE_EXT_CONTENT_INLINES is not None:
        try:
            for inline in settings.PAGES_PAGE_EXT_CONTENT_INLINES:
                PAGE_EXT_CONTENT_INLINES.append(importlib.import_module(inline))
        except ImportError as e:
            raise Exception('Extended content type inline import error: {0}'.format(e))


class PageAdmin(GuardedModelAdmin, MPTTModelAdmin):
    change_form_template = 'admin/pages/page/change_form.html'
    list_display = ['__str__',
                    'ptype',
                    'date_created_short', 'date_updated_short', 'date_approved_short',
                    'date_publication_short', 'date_publication_end_short']
    list_display_links = ['__str__']

    exclude = ('created_by', 'updated_by')
    readonly_fields = ('date_created', 'date_updated', 'date_approved')
    actions = ['make_draft', 'make_not_draft', 'make_approved', 'make_not_approved',
               'make_published', 'make_not_published']
    save_on_top = True
    actions_on_bottom = True

    page_fields = [
        ('name', ),
        ('ptype', ),
        ('parent', ),
        ('template', ),
    ]

    if hasattr(settings, 'SITE_ID'):
        if settings.PAGES_USE_SITE_ID:
            page_fields.append(('sites', ))

    fieldsets = [
        (None, {'fields': page_fields}),


        (_('State'), {'fields': [
            ('is_login_required', 'is_permission_required'),
            ('is_draft', 'is_approved', 'is_published'),
            ('date_created', 'date_updated', 'date_approved', ),
            ('date_publication', 'date_publication_end', ),
            ('comment',),
        ], 'classes': ['collapse']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(PageAdmin, self).get_form(request, obj, **kwargs)

    def get_all_content_inlines(self, object_id):
        inlines = []
        result = PageContent.objects.filter(page=object_id)
        content_types = [o.type for o in result]
        all_content_types = PageContentType.objects.all()
        content_class = None
        inlines.append(PageContentInline)
        for content_type in all_content_types:
            if content_type in content_types:
                class_name = content_type.admin_class_name
                try:
                    content_class = getattr(pagecontenttypes, class_name)
                    if not (issubclass(content_class, admin.TabularInline) or
                            issubclass(content_class, admin.StackedInline)):
                        content_class = None
                except AttributeError:
                    try:
                        if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
                            for module in PAGE_EXT_CONTENT_INLINES:
                                if hasattr(module, class_name):
                                    content_class = getattr(module, class_name)
                                    if not (issubclass(content_class, admin.TabularInline) or
                                            issubclass(content_class, admin.StackedInline)):
                                        content_class = None
                                    else:
                                        break
                    except AttributeError:
                        pass
                if content_class is not None:
                    inlines.append(content_class)
            content_class = None
        return inlines

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = self.get_all_content_inlines(object_id)
        return super(PageAdmin, self).change_view(request, object_id)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [PageContentInline]
        return super(PageAdmin, self).add_view(request)

    @staticmethod
    def __get_message_bit(rows_updated):
        if rows_updated == 1:
            message_bit = _('one pages was')
        else:
            message_bit = _('{0} pages were').format(rows_updated)
        return message_bit

    def make_draft(self, request, queryset):
        rows_updated = queryset.update(is_draft=True, is_approved=False, date_approved=None, is_published=False)
        self.message_user(request, _('{0} successfully marked as draft.').format(self.__get_message_bit(rows_updated)))
    make_draft.short_description = _('Mark selected pages as draft')

    def make_not_draft(self, request, queryset):
        rows_updated = queryset.update(is_draft=False)
        self.message_user(request, _('{0} successfully marked as not draft.').format(self.__get_message_bit(rows_updated)))
    make_not_draft.short_description = _('Mark selected pages as not draft')

    def make_approved(self, request, queryset):
        rows_updated = queryset.update(is_approved=True, date_approved=timezone.now, is_draft=False)
        message = _('{0} successfully marked as approved.').format(self.__get_message_bit(rows_updated))
        self.message_user(request, message)
    make_approved.short_description = _('Mark selected pages as approved')

    def make_not_approved(self, request, queryset):
        rows_updated = queryset.update(is_approved=False, date_approved=None, is_published=False)
        message = _('{0} successfully marked as not approved.').format(self.__get_message_bit(rows_updated))
        self.message_user(request, message)
    make_not_approved.short_description = _('Mark selected pages as not approved')

    def make_published(self, request, queryset):
        rows_updated = queryset.update(is_published=True, is_draft=False)
        message = _('{0} successfully marked as piblished.').format(self.__get_message_bit(rows_updated))
        self.message_user(request, message)
    make_published.short_description = _('Mark selected pages as published')

    def make_not_published(self, request, queryset):
        rows_updated = queryset.update(is_published=False)
        message = _('{0} successfully marked as not published.').format(self.__get_message_bit(rows_updated))
        self.message_user(request, message)
    make_not_published.short_description = _('Mark selected pages as not published')

    def date_created_short(self, obj):
        return obj.date_created.strftime('%Y/%m/%d %H:%M:%S')

    date_created_short.short_description = _('Created')
    date_created_short.admin_order_field = 'date_created'

    def date_updated_short(self, obj):
        return obj.date_updated.strftime('%Y/%m/%d %H:%M:%S')

    date_updated_short.short_description = _('Updated')
    date_updated_short.admin_order_field = 'date_updated'

    def date_approved_short(self, obj):
        date = None
        if obj.date_approved is not None:
            date = obj.date_approved.strftime('%Y/%m/%d %H:%M:%S')
        return date

    date_approved_short.short_description = _('Approved')
    date_approved_short.admin_order_field = 'date_approved'

    def date_publication_short(self, obj):
        date = None
        if obj.date_publication is not None:
            date = obj.date_publication.strftime('%Y/%m/%d %H:%M:%S')
        return date

    date_publication_short.short_description = _('Publication')
    date_publication_short.admin_order_field = 'date_publication'

    def date_publication_end_short(self, obj):
        date = None
        if obj.date_publication_end is not None:
            date = obj.date_publication_end.strftime('%Y/%m/%d %H:%M:%S')
        return date

    date_publication_end_short.short_description = _('Publication end')
    date_publication_end_short.admin_order_field = 'date_publication_end'

    def save_model(self, request, obj, form, change):
        """

        """
        if not change:
            obj.created_by = request.user

        obj.updated_by = request.user
        obj.save()

admin.site.register(Page, PageAdmin)
