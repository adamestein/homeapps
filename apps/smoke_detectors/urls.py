from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    'apps.smoke_detectors',
    url('^$', TemplateView.as_view(template_name='home.html'), name='smoke_detectors')
)
