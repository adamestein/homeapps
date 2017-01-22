from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import APP
from .forms import BatteryChangeEventForm, SmokeDetectorForm
from .models import BatteryChangeEvent, SmokeDetector

from library.views.generic import AppCreateView, AppDeleteMultipleView, AppListView, AppTemplateView, AppUpdateView

urlpatterns = patterns(
    'smoke_detectors',

    url('^$', AppTemplateView.as_view(template_name='smoke_detectors/home.html'), name='smoke_detectors'),

    url(
        '^add/$',
        AppCreateView.as_view(
            app=APP['name'],
            form_class=SmokeDetectorForm,
            model=SmokeDetector,
            success_message='Smoke detector \'%(location)s\' successfully added',
            success_url=reverse_lazy('list_smoke_detectors'),
            template_name='smoke_detectors/smokedetector_form.html'
        ),
        name='add_smoke_detector'
    ),

    url(
        '^add/event/$',
        AppCreateView.as_view(
            app=APP['name'],
            form_class=BatteryChangeEventForm,
            model=BatteryChangeEvent,
            success_message='Battery change event successfully added',
            success_url=reverse_lazy('list_smoke_detectors'),
            template_name='smoke_detectors/event_form.html'
        ),
        name='add_battery_change_event'
    ),

    url(
        '^delete/$',
        AppDeleteMultipleView.as_view(
            app=APP['name'],
            queryset=SmokeDetector.objects.all(),
            success_message='Smoke detector(s) have been deleted',
            success_url=reverse_lazy('list_smoke_detectors'),
            template_name='smoke_detectors/delete_form.html'
        ),
        name='delete_smoke_detectors'
    ),

    url(
        '^edit/$',
        AppListView.as_view(
            app=APP['name'],
            model=SmokeDetector,
            template_name='smoke_detectors/edit_list.html'
        ),
        name='edit_smoke_detector_list'
    ),

    url(
        '^edit/(?P<pk>[\d]+)$',
        AppUpdateView.as_view(
            app=APP['name'],
            form_class=SmokeDetectorForm,
            model=SmokeDetector,
            success_message='Smoke detector in %(location)s successfully updated',
            success_url=reverse_lazy('list_smoke_detectors'),
            template_name='smoke_detectors/smokedetector_form.html'
        ),
        name='edit_smoke_detector'
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
