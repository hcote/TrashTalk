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
    participants = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                                      queryset=User.objects.all())

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

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if key == 'location':
                for k, v in validated_data[key].items():
                    setattr(instance.location, k, v)
            elif key == 'participants':
                participant = validated_data[key][0]
                if participant not in instance.participants.all():
                    instance.participants.add(participant)
                else:
                    instance.participants.remove(participant)
            else:
                setattr(instance, key, val)
        instance.save()
        return instance
