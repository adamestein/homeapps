from django.conf.urls import patterns, url

from .models import SmokeDetector

from library.views.generic import NavigationListView, NavigationTemplateView

urlpatterns = patterns(
    'smoke_detectors',

    url('^$', NavigationTemplateView.as_view(template_name='smoke_detectors/home.html'), name='smoke_detectors'),

    url(
        '^list/$',
        NavigationListView.as_view(model=SmokeDetector, template_name='smoke_detectors/list.html'),
        name='list_smoke_detectors'
    )
)
