from django.conf.urls import patterns, url

from pages.views import PageDetailsView

urlpatterns = patterns('pages.views',
    # pages
    url(r'^page/(?P<slug>[-\w]+)/$', PageDetailsView.as_view(), name='page_show'),
)
