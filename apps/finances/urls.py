from django.conf.urls import patterns, url
from apps.views import HomePageView

urlpatterns = patterns(
    'apps.finances',
    url('^$', HomePageView.as_view(), name='finances')
)
