from threading import current_thread

_requests = {}


def get_user():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t].user


class RequestMiddleware(object):
    @staticmethod
    def process_request(request):
        _requests[current_thread()] = request
