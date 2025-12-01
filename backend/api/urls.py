from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserProfileView
from .views_dashboard import TestListView, UserAttemptListView
from .views_exam import StartTestView, SubmitAnswerView, SubmitTestView

# Redis-based exam timer views (production-ready)
from .views_exam_timer import (
    StartExamView,
    GetRemainingTimeView,
    SubmitAnswerView as SubmitAnswerTimerView,
    SubmitExamView,
    GetExamQuestionsView,
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Dashboard endpoints
    path('tests/', TestListView.as_view(), name='test_list'),
    path('attempts/', UserAttemptListView.as_view(), name='attempt_list'),
    
    # Legacy exam endpoints (without Redis timers)
    path('exam/start/<int:test_id>/', StartTestView.as_view(), name='start_test'),
    path('exam/submit-answer/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('exam/submit/', SubmitTestView.as_view(), name='submit_test'),
    
    # NEW: Production Redis-based exam timer endpoints
    path('exam/timer/start/<int:exam_id>/', StartExamView.as_view(), name='start_exam_timer'),
    path('exam/timer/remaining/<int:attempt_id>/', GetRemainingTimeView.as_view(), name='remaining_time'),
    path('exam/timer/submit-answer/', SubmitAnswerTimerView.as_view(), name='submit_answer_timer'),
    path('exam/timer/submit/<int:attempt_id>/', SubmitExamView.as_view(), name='submit_exam_timer'),
    path('exam/timer/questions/<int:attempt_id>/', GetExamQuestionsView.as_view(), name='exam_questions_timer'),
]
