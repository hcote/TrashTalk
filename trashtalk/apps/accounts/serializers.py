from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # TODO: Issue #86 -- Add validators for password
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)
