"""Django urls for content management system."""

from django.conf.urls import url

from pages.views import PageDetailsView

app_name = 'pages'
urlpatterns = [url(r'^(?P<slug>[-\w]+)/$', PageDetailsView.as_view(), name='show')]
