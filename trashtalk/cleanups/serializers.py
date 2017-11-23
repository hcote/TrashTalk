from rest_framework import serializers

from .models import Cleanup, Location


# pylint: disable=missing-docstring
class CleanupSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = Cleanup
        fields = ['id', 'name', 'description',
                  'start_time', 'end_time', 'location', 'host']


# pylint: disable=missing-docstring
class LocationSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = Location
        fields = ['id', 'number', 'street']
