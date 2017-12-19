import logging

from functools import wraps
from datetime import datetime

from django.http.response import HttpResponseForbidden

from cleanups.models import Cleanup

logger = logging.getLogger('core.utils')


def friendly_time(time):
    return datetime.strptime(str(time), '%X').strftime('%I:%M %p')


def iso_time(time):
    return datetime.strptime(str(time), '%I:%M %p').strftime('%X')


def host_required(view_func):
    @wraps(view_func)
    def is_event_host(request, *args, **kwargs):
        cleanup = Cleanup.objects.get(id=kwargs.get('pk'))
        if not cleanup.host == request.user:
            return HttpResponseForbidden()
        else:
            response = view_func(request, *args, **kwargs)
            return response

    return is_event_host
