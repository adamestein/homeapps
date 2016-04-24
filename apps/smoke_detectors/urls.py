from django.conf.urls import patterns, url
from apps.views import HomePageView

urlpatterns = patterns(
    'apps.smoke_detectors',
    url('^$', HomePageView.as_view(), name='smoke_detectors')
)
