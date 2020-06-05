from rest_framework import serializers

from users.models import User
from .models import Exercise


class ExerciseCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ExerciseSerializer(serializers.ModelSerializer):
    creator = ExerciseCreatorSerializer()

    class Meta:
        model = Exercise
        fields = ('id', 'creator', 'created_at', 'locale', 'title', 'content')
        read_only_fields = ('id', 'creator', 'created_at')

    def validate(self, attrs):
        locale = attrs['locale']
        locale_charset = Exercise.LOCALE_CHARSETS[locale]
        content = attrs['content']
        for char in content:
            if char not in locale_charset:
                print(repr(char))
                raise serializers.ValidationError(
                    f"The content contains the character \"{char}\" "
                    "forbidden within the given locale."
                )
        return attrs
