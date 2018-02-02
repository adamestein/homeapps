from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .mixins.navigation import NavigationContextMixin


class AppTemplateView(LoginRequiredMixin, NavigationContextMixin, TemplateView):
    pass
