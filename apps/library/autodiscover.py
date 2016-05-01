import copy
import json

from system_globals.models import SystemGlobal

from django.conf import settings
from django.contrib.admin.sites import site
from django.utils.importlib import import_module


def app_autodiscover():
    """
    Auto-discover INSTALLED_APPS information and fail silently when not present.
    """

    apps = {}

    for app in sorted(settings.INSTALLED_APPS):
        mod = import_module(app)
        before_import_registry = copy.copy(site._registry)
        try:
            import_module('%s.admin' % app)
        except ImportError:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            site._registry = before_import_registry
        else:
            # Get app info if there is any to get, otherwise ignore
            try:
                app_info = {'url_name': app.split('.')[-1]}
                app_info.update(mod.APP)
                # apps.append(app_info)
                apps[mod.APP['name']] = app_info
            except AttributeError:
                pass

    SystemGlobal.objects.set('apps', json.dumps(apps))
