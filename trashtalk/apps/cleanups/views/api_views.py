import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from cleanups.serializers import (Cleanup, CleanupSerializer,
                                  Location, LocationSerializer)

logger = logging.getLogger('cleanups.views')


# pylint: disable=missing-docstring
class CleanupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# pylint: disable=missing-docstring
class CleanupListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# pylint: disable=missing-docstring
class CleanupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


# pylint: disable=missing-docstring
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

