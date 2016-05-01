from django.views.generic import TemplateView

from .mixins import LoginRequiredMixin, NavigationContextMixin


class NavigationTemplateView(LoginRequiredMixin, NavigationContextMixin, TemplateView):
    pass
