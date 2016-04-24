from django.conf.urls import patterns, include, url

from apps.views import HomePageView

from django.contrib import admin
admin.autodiscover()

from library.autodiscover import app_autodiscover
app_autodiscover()

urlpatterns = patterns(
    '',

    # Admin URL patterns
    url(r'^admin/', include(admin.site.urls)),

    # Top level home page
    url(r'^$', HomePageView.as_view(), name='home'),

    # Apps
    url(r'^finances/', include('finances.urls')),
    url(r'^smoke_detectors/', include('smoke_detectors.urls')),
    url(r'^utilities/', include('utilities.urls'))
)
