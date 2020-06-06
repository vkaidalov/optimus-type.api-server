from typing import List

from rest_framework import serializers

from users.models import User
from . import validators
from .models import Exercise, Attempt


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ExerciseSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()

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


class AttemptExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'locale')
        read_only_fields = ('title', 'locale')


class AttemptListItemSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    exercise = AttemptExerciseSerializer(read_only=True)

    class Meta:
        model = Attempt
        fields = (
            'id', 'creator', 'exercise', 'created_at', 'layout',
            'time_spent', 'mistakes'
        )
        read_only_fields = fields


class AttemptDetailSerializer(AttemptListItemSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.filter(is_banned=False, is_removed=False),
        write_only=True, source='exercise'
    )
    mistake_time_logs = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        max_length=Attempt.MAX_MISTAKES
    )
    mistake_char_logs = serializers.CharField(
        max_length=Attempt.MAX_MISTAKES, allow_blank=True
    )

    class Meta(AttemptListItemSerializer.Meta):
        model = Attempt
        fields = AttemptListItemSerializer.Meta.fields + (
            'exercise_id', 'input_time_logs',
            'mistake_time_logs', 'mistake_char_logs',
        )
        read_only_fields = (
            'id', 'creator', 'exercise', 'created_at', 'time_spent', 'mistakes'
        )

    def validate_input_time_logs(self, value):  # noqa
        validators.unique_elements_sorted_in_asc(value)
        return value

    def validate_mistake_time_logs(self, value: List[int]):  # noqa
        validators.unique_elements_sorted_in_asc(value)
        return value

    def validate(self, attrs):
        exercise: Exercise = attrs['exercise']
        input_time_logs: List[int] = attrs['input_time_logs']
        mistake_time_logs: List[int] = attrs['mistake_time_logs']
        mistake_char_logs: str = attrs['mistake_char_logs']

        if len(exercise.content) != len(input_time_logs):
            raise serializers.ValidationError(
                "The length of the input_time_logs isn`t equal to "
                "the length of the exercise content."
            )

        if len(mistake_time_logs) != len(mistake_char_logs):
            raise serializers.ValidationError(
                "The length of the mistake_time_logs isn`t equal to "
                "the length of the mistake_char_logs."
            )

        if mistake_time_logs and mistake_time_logs[-1] >= input_time_logs[-1]:
            raise serializers.ValidationError(
                "The last element of the mistake_time_logs must be less than "
                "the last element of the input_time_logs."
            )

        if not (
                input_time_logs[0] == 0 or
                mistake_time_logs and mistake_time_logs[0] == 0
        ):
            raise serializers.ValidationError(
                "Either the first element of the input_time_logs or "
                "the first element of the mistake_time_logs must be 0."
            )

        if any(time_log in mistake_time_logs for time_log in input_time_logs):
            raise serializers.ValidationError(
                "The mistake_time_logs and the input_time_logs arrays must "
                "not have common elements."
            )

        return attrs

    def create(self, validated_data):
        # Set the `time_spent` field on the server side.
        input_time_logs: List[int] = validated_data['input_time_logs']
        time_spent = input_time_logs[-1]
        return Attempt.objects.create(time_spent=time_spent, **validated_data)
