import json

from system_globals.models import SystemGlobal

from django.conf import settings


# noinspection PyUnusedLocal
def apps(request):
    return {'apps': json.loads(SystemGlobal.objects.get_value('apps'))}


# noinspection PyUnusedLocal
def version(request):
    if settings.DEBUG:
        mode = "(Development) "
    else:
        mode = ""

    return {'version': 'Home Apps {}v{}'.format(mode, settings.VERSION)}
