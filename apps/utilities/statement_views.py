from django.http import Http404
from django.urls import reverse_lazy

from library.views.generic import AppCreateView

from .forms import ElectricGasStatementForm, WaterStatementForm
from .models import ElectricGasStatement, WaterStatement


class StatementAddView(AppCreateView):
    success_url = reverse_lazy('utilities:statement_select_type')
    template_name = 'utilities/statement/add.html'

    def dispatch(self, request, *args, **kwargs):
        statement_type = kwargs['statement_type']

        if statement_type == 'electric_gas':
            self.form_class = ElectricGasStatementForm
            self.model = ElectricGasStatement
        elif statement_type == 'water':
            self.form_class = WaterStatementForm
            self.model = WaterStatement
        else:
            raise Http404(f'Unknown statement type: {statement_type}')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statement_type'] = self.kwargs['statement_type']
        return context
