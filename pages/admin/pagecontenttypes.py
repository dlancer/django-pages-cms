"""Implements admin interface for page content"""

from django.contrib import admin

from pages.models import PageSlugContent
from pages.models import PageRedirectContent
from pages.models import PageMetaContent
from pages.models import PageTextContent
from pages.models import PageMarkdownContent


class PageSlugContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    list_display_links = ['__str__']

    exclude = ('type', 'sid', 'is_extended', 'created_by', 'updated_by',)
    save_on_top = True
    actions_on_bottom = True


admin.site.register(PageSlugContent, PageSlugContentAdmin)


class PageSlugContentInline(admin.StackedInline):
    model = PageSlugContent
    extra = 1
    exclude = ('sid', 'created_by', 'updated_by', 'date_created', 'date_updated', )
    fieldsets = [
        (None, {'fields': [
            ('language', ),
            ('name', ),
            ('slug', ),
            ('comment', ),
        ]}),
    ]


class PageRedirectContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    list_display_links = ['__str__']

    exclude = ('type', 'sid', 'is_extended', 'created_by', 'updated_by')
    save_on_top = True
    actions_on_bottom = True


admin.site.register(PageRedirectContent, PageRedirectContentAdmin)


class PageRedirectContentInline(admin.StackedInline):
    model = PageRedirectContent
    extra = 1
    exclude = ('sid', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    fieldsets = [
        (None, {'fields': [
            ('language', ),
            ('name', ),
            ('redirect_to_page', ),
            ('redirect_to_url', ),
            ('is_permanent', ),
            ('comment', ),
        ]}),
    ]


class PageMetaContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    list_display_links = ['__str__']

    exclude = ['type', 'sid', 'is_extended', 'created_by', 'updated_by']
    save_on_top = True
    actions_on_bottom = True


admin.site.register(PageMetaContent, PageMetaContentAdmin)


class PageMetaContentInline(admin.StackedInline):
    model = PageMetaContent
    extra = 1
    exclude = ('sid', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    fieldsets = [
        (None, {'fields': [
            ('language', ),
            ('name', ),
            ('title', ),
            ('keywords', ),
            ('description', ),
            ('is_noindex', 'is_nofollow', ),
            ('comment', ),
        ]}),
    ]


class PageTextContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    list_display_links = ['__str__']

    exclude = ('type', 'sid', 'is_extended', 'created_by', 'updated_by',)
    save_on_top = True
    actions_on_bottom = True


admin.site.register(PageTextContent, PageTextContentAdmin)


class PageTextContentInline(admin.StackedInline):
    model = PageTextContent
    extra = 1
    exclude = ('sid', 'created_by', 'updated_by', 'date_created', 'date_updated', )
    fieldsets = [
        (None, {'fields': [
            ('language', ),
            ('name', ),
            ('text', ),
            ('is_template', ),
            ('comment', ),
        ]}),
    ]


class PageMarkdownContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_by', 'updated_by', 'date_created', 'date_updated',)
    list_display_links = ['__str__']

    exclude = ('type', 'sid', 'is_extended', 'created_by', 'updated_by',)
    save_on_top = True
    actions_on_bottom = True


admin.site.register(PageMarkdownContent, PageMarkdownContentAdmin)


class PageMarkdownContentInline(admin.StackedInline):
    model = PageMarkdownContent
    extra = 1
    exclude = ('sid', 'created_by', 'updated_by', 'date_created', 'date_updated', )
    fieldsets = [
        (None, {'fields': [
            ('language', ),
            ('name', ),
            ('text', ),
            ('is_template', ),
            ('comment', ),
        ]}),
    ]
