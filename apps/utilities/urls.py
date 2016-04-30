from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    'utilities',
    url('^$', TemplateView.as_view(template_name='home.html'), name='utilities')
)
