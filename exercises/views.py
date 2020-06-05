from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from .models import Exercise
from .serializers import ExerciseSerializer


@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['exercises']))
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['exercises']))
class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.filter(is_banned=False, is_removed=False)
    serializer_class = ExerciseSerializer
