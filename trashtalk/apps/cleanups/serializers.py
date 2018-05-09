import logging
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from accounts.serializers import User
from .models import (
    Cleanup, Location, RequiredTool, Tool, ToolCategory
)

logger = logging.getLogger('cleanups.serializers')


# pylint: disable=missing-docstring
class ToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tool
        fields = ['id', 'category', 'description', 'image_static_location', 'name']


# pylint: disable=missing-docstring
class ToolCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ToolCategory
        fields = ['id', 'name', 'description']


# pylint: disable=missing-docstring
class RequiredToolSerializer(serializers.ModelSerializer):
    tool = serializers.IntegerField(source='tool.id')
    class Meta:
        model = RequiredTool
        fields = ['quantity', 'tool']

# pylint: disable=missing-docstring
class LocationSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longitude', 'image', 'number', 'query', 'street']


# pylint: disable=missing-docstring
class CleanupSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False)
    location = LocationSerializer(required=False)
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    participants = serializers.PrimaryKeyRelatedField(
        many=True, required=False,
        queryset=User.objects.all()
    )

    required_tools = RequiredToolSerializer(source='requiredtool_set', many=True, required=False)

    class Meta:
        model = Cleanup
        fields = ('id', 'title', 'description', 'image', 'participants',
                  'start', 'end', 'location', 'host', 'required_tools')
        depth = 1

    def create(self, validated_data):
        # TODO: Issue #97 -- Integrate with integrations.google_maps.api.geolocate
        location = Location.objects.create(**validated_data.pop('location'))
        if 'participants' in validated_data:
            participants = validated_data.pop('participants')
        required_tools = validated_data.pop('requiredtool_set') if 'requiredtool_set' in validated_data else []
        cleanup = Cleanup.objects.create(
            location=location,
            host=self.context['request'].user,
            **validated_data
        )

        for required_tool in required_tools:
            RequiredTool.objects.create(
                cleanup=cleanup,
                quantity=required_tool['quantity'],
                tool=get_object_or_404(Tool, pk=required_tool['tool']['id'])
            )

        return cleanup

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if key == 'location':
                for k, v in validated_data[key].items():
                    setattr(instance.location, k, v)
            elif key == 'participants':
                # only allow logged in user to modify him/herself in participants list
                user = self.context['request'].user
                updated_participants = validated_data[key]
                current_participants = instance.participants.all()
                if user not in updated_participants and user in current_participants:
                    instance.participants.remove(user.id)
                elif user in updated_participants and user not in current_participants:
                    instance.participants.add(user.id)
            elif key == 'requiredtool_set':
                # Remove all existing required tools before setting new ones
                RequiredTool.objects.filter(cleanup=instance).delete()

                for required_tool in validated_data[key]:
                    RequiredTool.objects.create(
                        cleanup=instance,
                        quantity=required_tool['quantity'],
                        tool=get_object_or_404(Tool, pk=required_tool['tool']['id'])
                    )
            else:
                setattr(instance, key, val)
        instance.save()
        return instance
