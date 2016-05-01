from django.views.generic import TemplateView

from .mixins import LoginRequiredMixin, NavigationContextMixin


class AppTemplateView(LoginRequiredMixin, NavigationContextMixin, TemplateView):
    pass
