from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    'finances',
    url('^$', TemplateView.as_view(template_name='home.html'), name='finances')
)
