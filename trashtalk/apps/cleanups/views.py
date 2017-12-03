import logging
from datetime import datetime

from django.shortcuts import get_object_or_404, get_list_or_404, render

from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import CleanupForm, CleanupFormSet
from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer

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


# pylint: disable=missing-docstring
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
