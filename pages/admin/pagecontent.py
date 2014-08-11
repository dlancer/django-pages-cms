from django.contrib import admin

from pages.models import PageContent


class PageContentInline(admin.StackedInline):
    model = PageContent

    # max_num = 1
    extra = 1


class PageContentAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_display_links = ['__str__']

    save_on_top = True
    actions_on_bottom = True

admin.site.register(PageContent, PageContentAdmin)
