from typing import List

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from users.models import User
from . import validators
from .models import Exercise, Attempt, FastestAttempt, LayoutStatistics


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ExerciseSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    content = serializers.CharField(
        max_length=Exercise.CONTENT_MAX_LENGTH,
        trim_whitespace=False
    )

    class Meta:
        model = Exercise
        fields = ('id', 'creator', 'created_at', 'locale',
                  'title', 'content', 'attempt_counter')
        read_only_fields = ('id', 'creator', 'created_at', 'attempt_counter')

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
        max_length=Attempt.MAX_MISTAKES, allow_blank=True,
        trim_whitespace=False
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
        mistake_char_logs: str = validated_data['mistake_char_logs']
        time_spent = input_time_logs[-1] - input_time_logs[0]

        exercise: Exercise = validated_data['exercise']
        exercise.attempt_counter = F('attempt_counter') + 1

        creator: User = validated_data['creator']
        try:
            fastest_attempt = FastestAttempt.objects.get(
                creator=creator, exercise=exercise
            )
        except FastestAttempt.DoesNotExist:
            fastest_attempt = FastestAttempt(
                creator=creator, exercise=exercise, time_spent=time_spent
            )

        layout: str = validated_data['layout']
        try:
            layout_stats = LayoutStatistics.objects.get(
                user=creator, layout=layout
            )
        except LayoutStatistics.DoesNotExist:
            layout_stats = LayoutStatistics(
                user=creator, layout=layout
            )
            # Save and initialize with zeroes to use F() below.
            layout_stats.save()
        layout_stats.attempt_counter = F('attempt_counter') + 1
        layout_stats.input_counter = F('input_counter') + len(exercise.content)
        layout_stats.mistake_counter = F('mistake_counter') + len(mistake_char_logs)
        layout_stats.delay_counter = F('delay_counter') + time_spent

        with transaction.atomic():
            exercise.save()
            attempt = Attempt.objects.create(time_spent=time_spent, **validated_data)
            # Save only if it is the new record or
            # if it is the first record at all.
            if time_spent <= fastest_attempt.time_spent:
                fastest_attempt.time_spent = time_spent
                fastest_attempt.attempt = attempt
                fastest_attempt.save()
            layout_stats.save()

        return attempt


class FastestAttemptSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)

    class Meta:
        model = FastestAttempt
        fields = ('id', 'creator', 'exercise', 'time_spent')
        read_only_fields = fields


class LayoutStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutStatistics
        fields = ('id', 'user', 'layout',
                  'attempt_counter', 'input_counter',
                  'mistake_counter', 'delay_counter')
        read_only_fields = fields
