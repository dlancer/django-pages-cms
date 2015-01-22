"""Implements admin interface for Pages"""

from django.contrib import admin

from pages.models import PageContentType


class PageContentTypeAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_display_links = ['__str__']
    save_on_top = True
    actions_on_bottom = True

admin.site.register(PageContentType, PageContentTypeAdmin)
