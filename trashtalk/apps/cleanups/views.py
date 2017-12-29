import logging
from copy import deepcopy
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.utils import host_required
from .factories import cleanup_factory
from .forms import CleanupFormSet
from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer, User

logger = logging.getLogger('cleanups.views')


@host_required
@login_required
def cleanup_edit(request, *args, **kwargs):
    logger.info("Edit user: %s", request.user)
    context = {'cleanup': get_object_or_404(Cleanup, id=kwargs['pk'])}
    return render(request, 'cleanups/edit.html', context)


def cleanup_show(request, *args, **kwargs):
    cleanup = get_object_or_404(Cleanup, id=kwargs['pk'])
    gmap = settings.GOOGLE_MAPS_EMBED + cleanup.gmap_query
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


# pylint: disable=missing-docstring
class CleanupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


# pylint: disable=missing-docstring
class CleanupListCreateView(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer

    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        location_data = {'street': data.pop('street')[0], 'number': data.pop('number')[0]}
        # TODO: Why req QueryDict wasn't passing location to serializer, forcing this approach
        cleanup = {
            'title': data.get('title'),
            'description': data.get('description'),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'date': data.get('date'),
            'host': data.get('host'),
            'location': location_data,
            'participants': data.get('participants')
        }

        try:
            serializer = self.get_serializer(data=cleanup)
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            logger.exception("Cleanup not created.")
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# pylint: disable=missing-docstring
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
