import logging
from rest_framework import serializers

from accounts.serializers import User
from .models import Cleanup, Location

logger = logging.getLogger('cleanups.serializers')


# pylint: disable=missing-docstring
class LocationSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = Location
        fields = ['id', 'number', 'street']


# pylint: disable=missing-docstring
class CleanupSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Cleanup
        fields = ('id', 'title', 'description', 'date', 'participants',
                  'start_time', 'end_time', 'location', 'host')
        depth = 1

    def create(self, validated_data):
        # TODO: Issue #97 -- Integrate with integrations.google_maps.api.geolocate
        location = Location.objects.create(**validated_data.pop('location'))
        cleanup = Cleanup.objects.create(location=location, **validated_data)
        return cleanup
