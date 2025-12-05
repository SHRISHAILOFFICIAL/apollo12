from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, SectionViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]
