from django.urls import include, path, re_path
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
    path('admin/', admin.site.urls),

    # Account URL patterns
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),

    re_path(r'^add/(?P<model_name>\w+)/?$', add_new_model),

    # Top level home page URL pattern
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Apps URL patterns
    path('finances/', include('finances.urls')),
    path('utilities/', include('utilities.urls'))
]
