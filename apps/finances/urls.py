from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import APP
from .forms import CreateTemplateMultiForm, UpdateTemplateForm
from .models import AccountTemplate
from .templates import TemplateCreateView, TemplateUpdateView, TemplateListView

from library.views.generic import AppTemplateView

urlpatterns = patterns(
    'finances',

    url('^$', AppTemplateView.as_view(template_name='finances/home.html'), name='finances'),

    url(
        '^create_template/$',
        TemplateCreateView.as_view(
            app=APP['name'],
            form_class=CreateTemplateMultiForm,
            success_message="Template '%(name)s' successfully created",
            success_url=reverse_lazy('list_templates'),
            template_name='finances/template_create_form.html'
        ),
        name='create_template'
    ),

    url(
        '^edit_template/$',
        TemplateListView.as_view(
            app=APP['name'],
            queryset=AccountTemplate.objects.none(),        # All template lists will be loaded in get_context_data()
            template_name='finances/edit_template_list.html'
        ),
        name='edit_template_list'
    ),

    url(
        '^edit_template/(?P<template_type>[a-z]+)/(?P<pk>[\d]+)$',
        TemplateUpdateView.as_view(
            app=APP['name'],
            form_class=UpdateTemplateForm,
            success_message="Template '%(name)s' successfully updated",
            success_url=reverse_lazy('list_templates'),
            template_name='finances/template_update_form.html'
        ),
        name='edit_template'
    ),

    url(
        '^list_templates/$',
        TemplateListView.as_view(
            app=APP['name'],
            queryset=AccountTemplate.objects.none(),        # All template lists will be loaded in get_context_data()
            template_name='finances/list_templates.html'
        ),
        name='list_templates'
    )
)
