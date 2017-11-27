import logging
from datetime import datetime

from django.shortcuts import get_object_or_404, get_list_or_404, render

from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import CleanupForm, CleanupFormSet
from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer

log = logging.getLogger('cleanups.views')


def cleanup_edit(request, cleanup_id):
    # context = {'cleanup': cleanups.filter(id=request.get('pk')).first()}
    context = {'cleanup': get_object_or_404(Cleanup, id=cleanup_id)}
    return render(request, 'cleanups/edit.html', context)


def cleanup_list(request):
    context = {'cleanups': get_list_or_404(Cleanup, end_time__gt=datetime.today())}
    return render(request, 'cleanups/list.html', context)


def cleanup_new(request):
    context = {'form': CleanupFormSet()}
    return render(request, 'cleanups/new.html', context)


# pylint: disable=missing-docstring
class CleanupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cleanups/detail.html'

    def get(self, request, *args, **kwargs):
        cleanup = self.get_object()
        log.info("Cleanup: %s", cleanup)
        return Response({'cleanup': cleanup}, template_name=self.template_name)


# pylint: disable=missing-docstring
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# pylint: disable=missing-docstring
class CleanupListCreateView(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer
