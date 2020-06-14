from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, filters
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer


@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['users'])
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['users'])
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
