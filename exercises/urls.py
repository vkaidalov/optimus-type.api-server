from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ExerciseViewSet, AttemptViewSet


router = DefaultRouter()
router.register('exercises', ExerciseViewSet)
router.register('attempts', AttemptViewSet)

urlpatterns = [
    path('', include(router.urls))
]
