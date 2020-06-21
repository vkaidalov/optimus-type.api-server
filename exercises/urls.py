from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('exercises', views.ExerciseViewSet)
router.register('attempts', views.AttemptViewSet)
router.register('fastest-attempts', views.FastestAttemptViewSet)
router.register('layout-statistics', views.LayoutStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
