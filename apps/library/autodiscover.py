import json

from system_globals.models import SystemGlobal

from django.apps import apps as django_apps


def app_autodiscover():
    """
    Auto-discover installed apps information and fail silently when not present.
    """

    apps = {}

    for app in django_apps.get_app_configs():
        app_settings = getattr(app.module, 'APP', None)
        if app_settings:
            apps[app_settings['name']] = app_settings
            apps[app_settings['name']].update({'url_name': app.label})

    SystemGlobal.objects.set('apps', json.dumps(apps))
