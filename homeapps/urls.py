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
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^add/(?P<model_name>\w+)/?$', 'tekextensions.views.add_new_model'),

    # Top level home page URL pattern
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Apps URL patterns
    url(r'^finances/', include('finances.urls')),
    url(r'^smoke_detectors/', include('smoke_detectors.urls')),
    url(r'^utilities/', include('utilities.urls'))
)
