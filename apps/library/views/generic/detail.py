from django.core.exceptions import ImproperlyConfigured
from django.views.generic import DetailView

from .mixins.auth import LoginRequiredMixin
from .mixins.navigation import NavigationContextMixin


class AppDetailView(LoginRequiredMixin, NavigationContextMixin, DetailView):
    queryset = None

    def get_queryset(self):
        """
        Get the queryset to look an object up against.  Add filtering by user.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.filter(user=self.request.user)
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a queryset. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        else:
            self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset._clone()
