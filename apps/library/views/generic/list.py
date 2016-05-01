from django.views.generic import ListView

from .mixins import LoginRequiredMixin, NavigationContextMixin


class AppListView(LoginRequiredMixin, NavigationContextMixin, ListView):
    pass
