from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

from tekextensions.views import add_new_model

from library.autodiscover import app_autodiscover
app_autodiscover()

admin.site.site_header = 'HomeApps'
admin.site.site_title = 'HomeApps'

urlpatterns = [
    # Admin URL patterns
    url(r'^admin/', admin.site.urls),

    # Account URL patterns
    # url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(next_page='/'), name='logout'),

    url(r'^add/(?P<model_name>\w+)/?$', add_new_model),

    # Top level home page URL pattern
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Apps URL patterns
    url(r'^finances/', include('finances.urls')),
    url(r'^smoke_detectors/', include('smoke_detectors.urls')),
    url(r'^utilities/', include('utilities.urls'))
]
