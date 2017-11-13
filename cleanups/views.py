from rest_framework import generics

from .serializers import Cleanup, CleanupSerializer, Location, LocationSerializer


class CleanupViews(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


class LocationViews(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
