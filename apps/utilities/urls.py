from django.conf.urls import patterns, url
from apps.views import HomePageView

urlpatterns = patterns(
    'apps.utilities',
    url('^$', HomePageView.as_view(), name='utilities')
)
