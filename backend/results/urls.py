from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamAttemptViewSet, AttemptResponseViewSet

router = DefaultRouter()
router.register(r'attempts', ExamAttemptViewSet, basename='attempt')
router.register(r'responses', AttemptResponseViewSet, basename='response')

urlpatterns = [
    path('', include(router.urls)),
]
