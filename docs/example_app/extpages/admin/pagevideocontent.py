"""Implements admin interface for page video content"""

from django.contrib import admin

from pages.conf import settings

if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
    from extpages.models.pagevideocontent import PageVideoContent
    from embed_video.admin import AdminVideoMixin

    class PageVideoContentAdmin(AdminVideoMixin, admin.ModelAdmin):
        list_display = ('__str__', 'created_by', 'updated_by', 'date_created', 'date_updated',)
        list_display_links = ['__str__']
        fieldsets = [
            (None, {'fields': [
                ('language', ),
                ('name', ),
                ('video', ),
                ('title', ),
                ('description', ),
                ('comment', ),
            ]}),
        ]

        exclude = ('type', 'sid', 'is_extended', 'created_by', 'updated_by',)
        save_on_top = True
        actions_on_bottom = True

    admin.site.register(PageVideoContent, PageVideoContentAdmin)

    class PageVideoContentInline(admin.StackedInline):
        model = PageVideoContent
        # max_num = 1
        extra = 1
        exclude = ('sid', 'is_extended', 'created_by', 'updated_by', 'date_created', 'date_updated',)
        fieldsets = [
            (None, {'fields': [
                ('language', ),
                ('name', ),
                ('video', ),
                ('title', ),
                ('description', ),
                ('comment', ),
            ]}),
        ]
