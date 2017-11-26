import logging

from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer

log = logging.getLogger('cleanups.views')


# pylint: disable=missing-docstring
class CleanupListCreateView(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


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
class LocationView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
