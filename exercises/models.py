from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.models import User
from . import constants


class Exercise(models.Model):
    LOCALES = (
        ('enUS', 'en_US'),
        ('ukUA', 'uk_UA'),
        ('ruRU', 'ru_RU')
    )

    LOCALE_CHARSETS = {
        "enUS": constants.EN_US_CHARSET,
        "ukUA": constants.UK_UA_CHARSET,
        "ruRU": constants.RU_RU_CHARSET
    }

    CONTENT_MAX_LENGTH = 1024

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    locale = models.CharField(max_length=4, choices=LOCALES)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    attempt_counter = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Attempt(models.Model):
    MAX_MISTAKES = 32

    LAYOUTS = (
        ('enUSAQ', 'en_US.Am.QWERTY'),
        ('enUSAD', 'en_US.Am.Dvorak'),
        ('enUSAC', 'en_US.Am.Colemak'),
        ('ukUAAЙ', 'uk_UA.Am.ЙЦУКЕН'),
        ('ruRUAЙ', 'ru_RU.Am.ЙЦУКЕН')
    )

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='attempts'
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='attempts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    layout = models.CharField(max_length=6, choices=LAYOUTS)
    input_time_logs = ArrayField(
        models.PositiveIntegerField(), size=Exercise.CONTENT_MAX_LENGTH
    )
    time_spent = models.PositiveIntegerField()
    mistake_time_logs = ArrayField(
        models.PositiveIntegerField(), size=MAX_MISTAKES
    )
    mistake_char_logs = models.CharField(max_length=MAX_MISTAKES)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return str(self.created_at)

    @property
    def mistakes(self) -> int:
        return len(self.mistake_char_logs)


class FastestAttempt(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    time_spent = models.PositiveIntegerField()

    class Meta:
        ordering = ('time_spent',)
        constraints = [
            models.UniqueConstraint(
                fields=['creator', 'exercise'],
                name='unique_fastest_attempt'
            )
        ]

    def __str__(self) -> str:
        return str(self.time_spent)


class LayoutStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    layout = models.CharField(max_length=6, choices=Attempt.LAYOUTS)
    attempt_counter = models.PositiveIntegerField(default=0)
    input_counter = models.PositiveIntegerField(default=0)
    mistake_counter = models.PositiveIntegerField(default=0)
    delay_counter = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('user', 'layout')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'layout'],
                name='unique_layout_statistics'
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
