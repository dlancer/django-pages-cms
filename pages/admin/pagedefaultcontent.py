from django.contrib import admin

from pages.models import PageDefaultContent


class PageDefaultContentAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_display_links = ['__str__']

    save_on_top = True
    actions_on_bottom = True


admin.site.register(PageDefaultContent, PageDefaultContentAdmin)
