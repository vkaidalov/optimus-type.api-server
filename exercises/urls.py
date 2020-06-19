from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ExerciseViewSet, AttemptViewSet, FastestAttemptViewSet


router = DefaultRouter()
router.register('exercises', ExerciseViewSet)
router.register('attempts', AttemptViewSet)
router.register('fastest-attempts', FastestAttemptViewSet)

urlpatterns = [
    path('', include(router.urls))
]
