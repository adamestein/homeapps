from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView

from .mixins import LoginRequiredMixin, NavigationContextMixin


class AppCreateView(LoginRequiredMixin, NavigationContextMixin, SuccessMessageMixin, CreateView):
    pass


class AppUpdateView(LoginRequiredMixin, NavigationContextMixin, SuccessMessageMixin, UpdateView):
    pass
