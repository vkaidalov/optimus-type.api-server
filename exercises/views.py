from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions

from .models import Exercise
from .serializers import ExerciseSerializer
from .permissions import IsCreatorOrReadOnly


@method_decorator(
    name='create', decorator=swagger_auto_schema(tags=['exercises'])
)
@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['exercises'])
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['exercises'])
)
@method_decorator(
    name='destroy', decorator=swagger_auto_schema(tags=['exercises'])
)
class ExerciseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Exercise.objects.filter(is_banned=False, is_removed=False)
    serializer_class = ExerciseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance: Exercise):
        instance.is_removed = True
        instance.save()
