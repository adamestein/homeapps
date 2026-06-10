from django.urls import path

from library.views.generic import AppTemplateView

from . import APP
from .data_views import DataListView
from .select_views import SelectView
from .statement_views import StatementAddView

app_name = 'utilities'
urlpatterns = [
    path('', AppTemplateView.as_view(template_name='utilities/home.html'), name='home'),

    path(
        'data/select/',
        SelectView.as_view(app=APP['name'], select='data'),
        name='data_select_type'
    ),

    path(
        'data/view/<str:data_type>',
        DataListView.as_view(
            app=APP['name'],
            template_name='utilities/data/view.html'
        ),
        name='view_data'
    ),

    path(
        'statement/add/<str:statement_type>/',
        StatementAddView.as_view(
            app=APP['name'],
            success_message='Added statement',
            template_name='utilities/statement/add.html'
        ),
        name='add_statement'
    ),

    path(
        'statement/select/',
        SelectView.as_view(app=APP['name'], select='statement'),
        name='statement_select_type'
    )
]
