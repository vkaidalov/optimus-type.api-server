from rest_framework import serializers

from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    locale = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ('id', 'creator', 'created_at', 'locale', 'title', 'content')

    def get_locale(self, obj):  # noqa
        return obj.get_locale_display()
