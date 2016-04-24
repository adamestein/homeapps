from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

from library.autodiscover import app_autodiscover
app_autodiscover()

urlpatterns = patterns(
    '',

    # Admin URL patterns
    url(r'^admin/', include(admin.site.urls)),

    # Account URL patterns
    url(r'^accounts/login/$', login, {'extra_context': {'next': '/'}}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),

    # Top level home page URL pattern
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Apps URL patterns
    url(r'^finances/', include('finances.urls')),
    url(r'^smoke_detectors/', include('smoke_detectors.urls')),
    url(r'^utilities/', include('utilities.urls'))
)
