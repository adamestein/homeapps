from django.views.generic import ListView

from .mixins.auth import LoginRequiredMixin
from .mixins.navigation import NavigationContextMixin


class AppListView(LoginRequiredMixin, NavigationContextMixin, ListView):
    pass
