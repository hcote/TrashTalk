import logging
from copy import deepcopy

from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .forms import CleanupFormSet
from .serializers import (Cleanup, CleanupSerializer, Location,
                          LocationSerializer)

log = logging.getLogger('cleanups.views')


def cleanup_edit(request, *args, **kwargs):
    context = {'cleanup': get_object_or_404(Cleanup, id=kwargs['pk'])}
    return render(request, 'cleanups/edit.html', context)


def cleanup_show(request, *args, **kwargs):
    context = {'cleanup': get_object_or_404(Cleanup, id=kwargs['pk'])}
    return render(request, 'cleanups/detail.html', context)


def cleanup_list(request):
    # TODO: Issue #86 - Filter, return only upcoming cleanups
    context = {'cleanups': get_list_or_404(Cleanup)}
    return render(request, 'cleanups/list.html', context)


def cleanup_new(request):
    context = {'form': CleanupFormSet()}
    return render(request, 'cleanups/new.html', context)


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
            'host': data.get('host'),
            'location': location_data
        }

        log.debug("Cleanup: %s", cleanup)
        try:
            serializer = self.get_serializer(data=cleanup)
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            log.exception("Cleanup not created.")
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# pylint: disable=missing-docstring
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
