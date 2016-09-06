from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import APP
from .models import AccountTemplate, Statement
from .statement_forms import CreateUpdateStatementMultiForm
from .statement_views import (
    StatementCreateView, StatementDetailView, StatementListView, StatementPDFView, StatementSectionForm,
    StatementSectionFormValidation, StatementUpdateView
)
from .template_forms import CreateTemplateMultiForm, UpdateTemplateForm
from .template_views import TemplateCreateView, TemplateUpdateView, TemplateListView
from .tracker_view import ChangeBillState, SavePaymentInfo, TrackableList, TrackerUpdateView

from library.views.generic import AppTemplateView

urlpatterns = patterns(
    'finances',

    url('^$', AppTemplateView.as_view(template_name='finances/home.html'), name='finances'),

    url(
        '^statement/create/$',
        StatementCreateView.as_view(
            app=APP['name'],
            form_class=CreateUpdateStatementMultiForm,
            success_message="Statement for %(date)s successfully created",
            template_name='finances/statement/create_update_form.html'
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
        '^statement/edit/$',
        StatementListView.as_view(
            action='edit',
            app=APP['name'],
            queryset=Statement.objects.all(),
            template_name='finances/statement/list.html'
        ),
        name='edit_statement_list'
    ),

    url(
        '^statement/edit/(?P<pk>[\d]+)$',
        StatementUpdateView.as_view(
            app=APP['name'],
            form_class=CreateUpdateStatementMultiForm,
            success_message="Statement for '%(date)s' successfully updated",
            template_name='finances/statement/create_update_form.html'
        ),
        name='edit_statement'
    ),

    url(
        '^statement/list/$',
        StatementListView.as_view(
            action='view',
            app=APP['name'],
            queryset=Statement.objects.all(),
            template_name='finances/statement/list.html'
        ),
        name='list_statements'
    ),

    url(
        '^statement/pdf/(?P<pk>[\d]+)/$',
        StatementPDFView.as_view(),
        name='statement_pdf'
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
    ),

    url(
        r'^tracker/(?P<pk>\d+)$',
        TrackerUpdateView.as_view(
            app=APP['name'],
            model=Statement,
            template_name='finances/tracker/tracker.html'
        ),
        name='tracker'
    ),

    url(
        '^tracker/bill_state/$',
        ChangeBillState.as_view(),
        name='change_bill_state'
    ),

    url(
        '^tracker/list/$',
        TrackableList.as_view(
            app=APP['name'],
            template_name='finances/tracker/list.html'
        ),
        name='trackable_list'
    ),

    url(
        '^tracker/validate/$',
        SavePaymentInfo.as_view(),
        name='save_payment_info'
    )
)
