from django.views.generic import ListView

from .mixins import LoginRequiredMixin, NavigationContextMixin


class NavigationListView(LoginRequiredMixin, NavigationContextMixin, ListView):
    pass
