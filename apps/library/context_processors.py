from collections import OrderedDict

from constance import config


# noinspection PyUnusedLocal
def apps(request):
    app_list = config.APPS

    # Put the dictionary in order by app name
    sorted_dict = OrderedDict()
    for name in sorted(app_list.keys()):
        sorted_dict[name] = app_list[name]

    return {'apps': sorted_dict}
