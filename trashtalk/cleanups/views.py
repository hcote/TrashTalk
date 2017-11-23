from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer


# pylint: disable=missing-
class HomeViews(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


# pylint: disable=missing-docstring
class CleanupViews(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


# pylint: disable=missing-docstring
class LocationViews(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
