import logging
from copy import deepcopy
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

from core.utils import host_required
from cleanups.factories import cleanup_factory
from cleanups.forms import CleanupFormSet
from cleanups.serializers import Cleanup, Location, User

logger = logging.getLogger('cleanups.views')


@host_required
@login_required
def cleanup_edit(request, *args, **kwargs):
    logger.info("Edit user: %s", request.user)
    context = {'cleanup': get_object_or_404(Cleanup, id=kwargs['pk'])}
    return render(request, 'cleanups/edit.html', context)


def cleanup_show(request, *args, **kwargs):
    cleanup = get_object_or_404(Cleanup, id=kwargs['pk'])
    gmap = settings.GOOGLE_MAPS_ENDPOINT + cleanup.gmap_query
    return render(request, 'cleanups/detail.html', {'cleanup': cleanup, 'gmap': gmap})


def cleanup_list(request):
    cleanups = Cleanup.objects.all().filter(date__gte=datetime.now())
    context = {'cleanups': cleanups}
    return render(request, 'cleanups/list.html', context)


@login_required
def cleanup_new(request):
    context = {'form': CleanupFormSet()}
    return render(request, 'cleanups/new.html', context)


@login_required
def cleanup_create(request):
    try:
        cleanup_data = cleanup_factory(deepcopy(request.POST))
        cleanup_data['location'] = Location.objects.create(**cleanup_data.get('location'))
    except (ObjectDoesNotExist, AttributeError):
        logger.exception('Error while creating a cleanup or location.')
        return HttpResponseBadRequest()
    else:
        cleanup = Cleanup.objects.create(**cleanup_data)
        return render(request, 'cleanups/detail.html', {'user': request.user,
                                                        'cleanup': cleanup})


@login_required
@api_view(['PATCH', 'POST', 'PUT'])
def cleanup_join_view(request, *args, **kwargs):
    cleanup = Cleanup.objects.get(id=kwargs.get('pk'))
    participant = User.objects.get(username=request.POST.get('participants'))
    if participant in cleanup.participants.all():
        cleanup.participants.remove(participant)
    else:
        cleanup.participants.add(participant)
    cleanup.save()
    return render(request, 'cleanups/detail.html',
                  {'cleanup': cleanup, 'participants': cleanup.participants.all()})


@host_required
@api_view(['POST', 'PUT', 'PATCH'])
def cleanup_update(request, *args, **kwargs):
    cleanup_data = cleanup_factory(deepcopy(request.data))
    Location.objects.filter(cleanup=kwargs['pk']).update(**cleanup_data.pop('location'))
    Cleanup.objects.filter(id=kwargs['pk']).update(**cleanup_data)
    cleanup = Cleanup.objects.get(id=kwargs['pk'])
    return render(request, 'cleanups/detail.html',
                  {'cleanup': cleanup, 'participants': cleanup.participants.all()})
