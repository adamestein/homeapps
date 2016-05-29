from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import APP
from .forms import AddAccountTemplateForm, UpdateAccountTemplateForm
from .models import AccountTemplate

from library.views.generic import AppCreateView, AppListView, AppTemplateView, AppUpdateView

urlpatterns = patterns(
    'finances',

    url('^$', AppTemplateView.as_view(template_name='finances/home.html'), name='finances'),

    url(
        '^add_template/$',
        AppCreateView.as_view(
            app=APP['name'],
            form_class=AddAccountTemplateForm,
            model=AccountTemplate,
            success_message="Template '%(name)s' successfully added",
            success_url=reverse_lazy('list_templates'),
            template_name='finances/template_form.html'
        ),
        name='add_template'
    ),

    url(
        '^edit_template/$',
        AppListView.as_view(
            app=APP['name'],
            model=AccountTemplate,
            template_name='finances/edit_template_list.html'
        ),
        name='edit_template_list'
    ),

    url(
        '^edit_template/(?P<pk>[\d]+)$',
        AppUpdateView.as_view(
            app=APP['name'],
            form_class=UpdateAccountTemplateForm,
            model=AccountTemplate,
            success_message="Template '%(name)s' successfully updated",
            success_url=reverse_lazy('list_templates'),
            template_name='finances/template_form.html'
        ),
        name='edit_template'
    ),

    url(
        '^list_templates/$',
        AppListView.as_view(
            app=APP['name'],
            model=AccountTemplate,
            queryset=AccountTemplate.objects.exclude(disabled=True),
            template_name='finances/list_templates.html'
        ),
        name='list_templates'
    )
)
