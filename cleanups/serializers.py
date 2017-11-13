from rest_framework import serializers

from .models import Cleanup, Location


class CleanupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleanup
        fields = ['id', 'name', 'description',
                  'start_time', 'end_time', 'location', 'host']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'number', 'street']
