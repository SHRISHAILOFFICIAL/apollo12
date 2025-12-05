from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, UserProfileView
from .views_dashboard import ExamListView, UserAttemptListView
from .views_exam import StartExamView as StartExamLegacyView, SubmitAnswerView, SubmitExamView as SubmitExamLegacyView
from .jwt_views import CustomTokenObtainPairView

# Redis-based exam timer views (production-ready)
from .views_exam_timer import (
    StartExamView,
    GetRemainingTimeView,
    SubmitAnswerView as SubmitAnswerTimerView,
    SubmitExamView,
    GetExamQuestionsView,
)

# Question issue reporting
from .views_question_issue import ReportQuestionIssueView

# Results and dashboard
from .views_results import AttemptResultsView, UserDashboardView

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Dashboard endpoints
    path('exams/', ExamListView.as_view(), name='exam_list'),
    path('attempts/', UserAttemptListView.as_view(), name='attempt_list'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    
    # Legacy exam endpoints (without Redis timers)
    path('exam/start/<int:exam_id>/', StartExamLegacyView.as_view(), name='start_exam'),
    path('exam/submit-answer/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('exam/submit/', SubmitExamLegacyView.as_view(), name='submit_exam'),
    
    # NEW: Production Redis-based exam timer endpoints
    path('exam/timer/start/<int:exam_id>/', StartExamView.as_view(), name='start_exam_timer'),
    path('exam/timer/remaining/<int:attempt_id>/', GetRemainingTimeView.as_view(), name='remaining_time'),
    path('exam/timer/submit-answer/', SubmitAnswerTimerView.as_view(), name='submit_answer_timer'),
    path('exam/timer/submit/<int:attempt_id>/', SubmitExamView.as_view(), name='submit_exam_timer'),
    path('exam/timer/questions/<int:attempt_id>/', GetExamQuestionsView.as_view(), name='exam_questions_timer'),
    
    # Report issue endpoint
    path('exam/report-issue/', ReportQuestionIssueView.as_view(), name='report_question_issue'),
    
    # Results endpoint
    path('results/<int:attempt_id>/', AttemptResultsView.as_view(), name='attempt_results'),
]


