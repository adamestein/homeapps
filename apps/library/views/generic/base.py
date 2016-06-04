from django.views.generic import TemplateView

from .mixins.auth import LoginRequiredMixin
from .mixins.navigation import NavigationContextMixin


class AppTemplateView(LoginRequiredMixin, NavigationContextMixin, TemplateView):
    pass
