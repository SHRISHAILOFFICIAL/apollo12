from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttemptViewSet, AttemptAnswerViewSet

router = DefaultRouter()
router.register(r'attempts', AttemptViewSet, basename='attempt')
router.register(r'answers', AttemptAnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]
