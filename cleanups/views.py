from rest_framework import generics

from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer


# pylint: disable=missing-docstring
class CleanupViews(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


# pylint: disable=missing-docstring
class LocationViews(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
