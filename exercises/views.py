from rest_framework import viewsets

from .models import Exercise
from .serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.filter(is_banned=False, is_removed=False)
    serializer_class = ExerciseSerializer
