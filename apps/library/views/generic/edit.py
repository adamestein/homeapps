from django.views.generic import CreateView

from .mixins import LoginRequiredMixin, NavigationContextMixin


class AppCreateView(LoginRequiredMixin, NavigationContextMixin, CreateView):
    pass
