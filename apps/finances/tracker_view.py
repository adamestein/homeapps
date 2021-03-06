import json
import re

from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.views.generic import TemplateView

from library.views.generic import AppListView, AppUpdateView
from library.views.generic.mixins.ajax import AJAXResponseMixin

from .models import Bill, Statement
from .tracker_forms import TrackerBillForm


class ChangeBillState(AJAXResponseMixin, TemplateView):
    bill = None
    is_paid_state = False

    def get_context_data(self, **kwargs):
        return {}

    def post(self, request, *args, **kwargs):
        self.bill = Bill.objects.get(pk=request.POST['bill_id'])
        self.bill.state = int(request.POST['new_state'])
        self.bill.save()

        self.is_paid_state = self.bill.in_paid_state

        return super(ChangeBillState, self).post(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        text = self.bill.tracker_display_paid if self.is_paid_state else ''
        return HttpResponse(json.dumps([text, self.bill.options.all().count() > 0]))


class TrackableList(AppListView):
    def get_queryset(self):
        # Look for statements that have any bills in an unfunded or unpaid state
        state_query = Q(bill__state=Bill.STATE_UNFUNDED) | Q(bill__state=Bill.STATE_UNPAID)
        return Statement.objects.filter(state_query, user=self.request.user).distinct()


class TrackerUpdateView(AppUpdateView):
    # Somehow TrackerUpdateView (and hence AppUpdateView) is derived from ModelFormMixin and so therefore
    # needs an attribute called 'fields' (even though in this case, it's not used)
    fields = []

    def get_context_data(self, **kwargs):
        # Any bill that is in the unfunded (default) state and has the Auto Transfer option automatically goes
        # into the unpaid state since the bill will be funded automatically
        queryset = Bill.objects.filter(statement__id=self.kwargs['pk'])

        for bill in queryset:
            # Need to make sure the bill is in the unfunded state as we can be going to the Tracker again after
            # paying bills
            if bill.state == Bill.STATE_UNFUNDED and bill.has_auto_transfer:
                bill.state = Bill.STATE_UNPAID
                bill.save()

        context = super(TrackerUpdateView, self).get_context_data(**kwargs)
        bill_formset = modelformset_factory(Bill, form=TrackerBillForm, extra=0)
        context['formset'] = bill_formset(queryset=queryset)
        return context


class SavePaymentInfo(AJAXResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        # Figure out the prefix to use when creating the form. We do this by finding the pk POST entry and
        # getting the prefix form that key name. Couldn't get the id field to show up in the form, so the pk
        # field was added which is set to the id value.
        p = re.compile('(form-[0-9]+)-.*')
        prefix = p.search([x for x in list(self.request.POST.keys()) if x.endswith('-pk')][0]).group(1)

        form = TrackerBillForm(
            self.request.POST, prefix=prefix, instance=Bill.objects.get(pk=self.request.POST[prefix + '-pk'])
        )

        if form.is_valid():
            ret = ''
            form.save()
        else:
            ret = str(form)

        return ret
