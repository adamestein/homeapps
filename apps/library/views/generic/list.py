from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .mixins.navigation import NavigationContextMixin


class AppListView(LoginRequiredMixin, NavigationContextMixin, ListView):
    pass
