import djoser.serializers
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AuthUserSerializer(djoser.serializers.UserSerializer):
    pass
