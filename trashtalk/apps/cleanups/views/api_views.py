import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from  cleanups.models import (
    Cleanup, Location, RequiredTool, Tool, ToolCategory
)

from cleanups.serializers import (CleanupSerializer,
                                  LocationSerializer,
                                  ToolSerializer, ToolCategorySerializer,
                                  RequiredToolSerializer)

logger = logging.getLogger('cleanups.views')


# pylint: disable=missing-docstring
class CleanupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)


# pylint: disable=missing-docstring
class CleanupListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)


# pylint: disable=missing-docstring
class CleanupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleanup.objects.all()
    serializer_class = CleanupSerializer


# pylint: disable=missing-docstring
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# pylint: disable=missing-docstring
class ToolView(generics.ListAPIView):
    queryset = Tool.objects.filter(is_available=True)
    serializer_class = ToolSerializer


# pylint: disable=missing-docstring
class ToolCategoryView(generics.ListAPIView):
    queryset = ToolCategory.objects.filter()
    serializer_class = ToolCategorySerializer