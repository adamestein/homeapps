from collections import OrderedDict
import json

from system_globals.models import SystemGlobal

from django.conf import settings


# noinspection PyUnusedLocal
def apps(request):
    app_list = json.loads(SystemGlobal.objects.get_value('apps'))

    # Put the dictionary in order by app name
    sorted_dict = OrderedDict()
    for name in sorted(app_list.keys()):
        sorted_dict[name] = app_list[name]

    return {'apps': sorted_dict}
