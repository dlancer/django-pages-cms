from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from pages.conf import settings as pages_settings
from pages.views import PageDetailsView

admin.autodiscover()

urlpatterns = [
    url(r'^$', PageDetailsView.as_view(), kwargs={pages_settings.PAGES_PAGE_SLUG_NAME: 'home', }),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markitup/', include('markitup.urls'))
]

urlpatterns += i18n_patterns(url(r'^page/', include('pages.urls', namespace='pages')), )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
