from django.conf.urls import patterns, url

from library.views.generic import NavigationTemplateView

urlpatterns = patterns(
    'smoke_detectors',

    # Top page
    url('^$', NavigationTemplateView.as_view(template_name='smoke_detectors/home.html'), name='smoke_detectors')
)
