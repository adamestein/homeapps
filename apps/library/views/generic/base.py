from django.views.generic import TemplateView

from .mixins import LoginRequiredMixin


class NavigationTemplateView(LoginRequiredMixin, TemplateView):
    navigation = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationTemplateView, self).get_context_data(**kwargs)

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context
