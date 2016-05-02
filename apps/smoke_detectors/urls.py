from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import APP
from .models import SmokeDetector

from library.views.generic import AppCreateView, AppListView, AppTemplateView, AppUpdateView

urlpatterns = patterns(
    'smoke_detectors',

    url('^$', AppTemplateView.as_view(template_name='smoke_detectors/home.html'), name='smoke_detectors'),

    url(
        '^add/$',
        AppCreateView.as_view(
            app=APP['name'],
            model=SmokeDetector,
            success_message='Smoke detector in %(location)s successfully added',
            success_url=reverse_lazy('list_smoke_detectors'),
            template_name='smoke_detectors/form.html'
        ),
        name='add_smoke_detector'
    ),

    url(
        '^list/$',
        AppListView.as_view(
            app=APP['name'],
            model=SmokeDetector,
            template_name='smoke_detectors/list.html'
        ),
        name='list_smoke_detectors'
    )
)
