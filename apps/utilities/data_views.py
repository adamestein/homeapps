import plotly.graph_objects as go
import plotly.offline as opy

from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth
from django.http import Http404

from library.views.generic import AppListView

from .models import ElectricGasStatement, WaterStatement


class DataListView(AppListView):
    data_type = None

    def dispatch(self, request, *args, **kwargs):
        self.data_type = kwargs['data_type']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.data_type == 'electric_gas':
            context['data_type'] = 'Electric/Gas'
            context['years'] = ElectricGasStatement.objects\
                .filter(user=self.request.user)\
                .dates('statement_date', 'year') \
                .values_list('statement_date__year', flat=True)
        elif self.data_type == 'water':
            context['data_type'] = 'Water'
            context['years'] = WaterStatement.objects\
                .filter(user=self.request.user)\
                .dates('to_date', 'year') \
                .values_list('to_date__year', flat=True)
        else:
            raise Http404(f'Unknown data type: {self.data_type}')

        try:
            context['selected_year'] = int(self.request.GET.get('year'))
        except (TypeError, ValueError):
            context['selected_year'] = None

        context['graphs_template'] = f'utilities/data/views/graphs.html'
        context['raw_data_template'] = f'utilities/data/views/raw_data.html'
        context['stats_template'] = f'utilities/data/views/stats.html'

        if self.object_list:
            context['graphs'] = self._create_graphs()
            context['stats'] = self.object_list.aggregate(average=Avg('amount'), total=Sum('amount'))

        return context

    def get_queryset(self):
        year = self.request.GET.get('year')

        if year:
            if self.data_type == 'electric_gas':
                field = 'statement_date'
                queryset = ElectricGasStatement.objects.filter(user=self.request.user)
            elif self.data_type == 'water':
                field = 'to_date'
                queryset = WaterStatement.objects.filter(user=self.request.user)
            else:
                raise Http404(f'Unknown data type: {self.data_type}')

            queryset = queryset.filter(**{field + '__year': year})

            return queryset
        else:
            return None

    @staticmethod
    def _create_amount_graph(monthly, xlabels):
        figure = go.Figure(
            data=[
                go.Scatter(
                    x=xlabels,
                    y=[float(month["total_amount"] or 0) for month in monthly],
                    mode='lines+markers'
                )
            ]
        )

        figure.update_layout(
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            template='plotly_white'
        )

        return opy.plot(figure, auto_open=False, config={'responsive': True}, output_type='div')

    def _create_graphs(self):
        if self.data_type == 'electric_gas':
            monthly = self.object_list.annotate(month=TruncMonth("statement_date")) \
                .values("month") \
                .annotate(
                total_amount=Sum("amount"),
                total_electric=Sum("electric_used"),
                total_gas=Sum("gas_used"),
            )
        elif self.data_type == 'water':
            monthly = self.object_list.annotate(month=TruncMonth("to_date")) \
                .values("month") \
                .annotate(
                total_amount=Sum("amount"),
                total_water=Sum("water_used")
            )
        else:
            raise Http404(f'Unknown data type: {self.data_type}')

        monthly = monthly.order_by('month')
        xlabels = [month['month'].strftime('%b') for month in monthly]
        graphs = {'amount': self._create_amount_graph(monthly, xlabels)}

        if self.data_type == 'electric_gas':
            graphs['electric_usage'] = self._create_usage_graph(monthly, xlabels, 'total_electric', 'kWh')
            graphs['gas_usage'] = self._create_usage_graph(monthly, xlabels, 'total_gas', 'ccf')
        else:
            graphs['water_usage'] = self._create_usage_graph(monthly, xlabels, 'total_water', 'units')

        return graphs

    @staticmethod
    def _create_usage_graph(monthly, xlabels, field, yaxis_title):
        figure = go.Figure(
            data=[
                go.Bar(
                    x=xlabels,
                    y=[int(month[field] or 0) for month in monthly]
                )
            ]
        )

        figure.update_layout(
            xaxis_title='Month',
            yaxis_title=yaxis_title,
            template='plotly_white'
        )

        return opy.plot(figure, auto_open=False, config={'responsive': True}, output_type='div')
