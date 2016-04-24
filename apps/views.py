import json

from django.views.generic.base import TemplateView

from system_globals.models import SystemGlobal


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['apps'] = json.loads(SystemGlobal.objects.get_value('apps'))
        return context
