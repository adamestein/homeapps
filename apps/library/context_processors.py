from django.conf import settings


# noinspection PyUnusedLocal
def version(request):
    if settings.DEBUG:
        mode = "(Development) "
    else:
        mode = ""

    version_dict = {
        "version": "Home Apps %sv" % mode + settings.VERSION
    }

    return version_dict
