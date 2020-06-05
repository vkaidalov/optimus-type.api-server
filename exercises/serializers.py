from rest_framework import serializers

from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
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
