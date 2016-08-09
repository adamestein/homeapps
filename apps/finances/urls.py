from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import APP
from .statement_forms import CreateStatementMultiForm
from .template_forms import CreateTemplateMultiForm, UpdateTemplateForm
from .models import AccountTemplate, Statement
from .statement_views import (
    StatementCreateView, StatementDetailView, StatementListView, StatementSectionForm, StatementSectionFormValidation
)
from .template_views import TemplateCreateView, TemplateUpdateView, TemplateListView

from library.views.generic import AppTemplateView

urlpatterns = patterns(
    'finances',

    url('^$', AppTemplateView.as_view(template_name='finances/home.html'), name='finances'),

    url(
        '^statement/create/$',
        StatementCreateView.as_view(
            app=APP['name'],
            form_class=CreateStatementMultiForm,
            success_message="Statement for '%(date)s' successfully created",
            success_url=reverse_lazy('statement_detail'),
            template_name='finances/statement/create_form.html'
        ),
        name='create_statement'
    ),

     url(
        '^statement/detail/(?P<pk>\d+)$',
        StatementDetailView.as_view(
            app=APP['name'],
            model=Statement,
            template_name='finances/statement/detail.html'
        ),
        name='statement_detail'
    ),

    url(
        '^statement/section_form/$',
        StatementSectionForm.as_view(),
        name='get_statement_section_form'
    ),

    url(
        '^statement/section_form/validation/$',
        StatementSectionFormValidation.as_view(),
        name='statement_section_form_validation'
    ),

    url(
        '^statement/view/$',
        StatementListView.as_view(
            app=APP['name'],
            queryset=Statement.objects.all(),
            template_name='finances/statement/list.html'
        ),
        name='view_statement_list'
    ),

    url(
        '^template/create/$',
        TemplateCreateView.as_view(
            app=APP['name'],
            form_class=CreateTemplateMultiForm,
            success_message="Template '%(name)s' successfully created",
            success_url=reverse_lazy('list_templates'),
            template_name='finances/template/create_form.html'
        ),
        name='create_template'
    ),

    url(
        '^template/edit/$',
        TemplateListView.as_view(
            app=APP['name'],
            queryset=AccountTemplate.objects.none(),        # All template lists will be loaded in get_context_data()
            template_name='finances/template/edit_list.html'
        ),
        name='edit_template_list'
    ),

    url(
        '^template/edit/(?P<template_type>[a-z]+)/(?P<pk>[\d]+)$',
        TemplateUpdateView.as_view(
            app=APP['name'],
            form_class=UpdateTemplateForm,
            success_message="Template '%(name)s' successfully updated",
            success_url=reverse_lazy('list_templates'),
            template_name='finances/template/update_form.html'
        ),
        name='edit_template'
    ),

    url(
        '^template/list/$',
        TemplateListView.as_view(
            app=APP['name'],
            queryset=AccountTemplate.objects.none(),        # All template lists will be loaded in get_context_data()
            template_name='finances/template/list.html'
        ),
        name='list_templates'
    )
)
