from threading import current_thread

_requests = {}


def get_user():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t].user


class RequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_view(request, *args):
        _requests[current_thread()] = request
        return None
