from rest_framework import serializers

from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'creator', 'created_at', 'locale', 'title', 'content')
        read_only_fields = ('id', 'creator', 'created_at')
