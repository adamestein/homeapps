import json

from system_globals.models import SystemGlobal

from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin


class NavigationContextMixin(ContextMixin):
    app = None
    request = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationContextMixin, self).get_context_data(**kwargs)

        # Add web page navigation if we have it
        if self.app:
            try:
                # Look for a match for the URL path we are at. The match should not be clickable since we ARE at
                # that page.
                nav_info = json.loads(SystemGlobal.objects.get_value('apps'))[self.app]['navigation']
                for info in nav_info:
                    if info and info['link']:
                        if self.request.path == reverse(info['link']):
                            info['link'] = None
            except KeyError:
                pass
            else:
                context["navigation"] = nav_info

        return context
