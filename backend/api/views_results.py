from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Avg
from datetime import datetime

from results.models import Attempt, AttemptAnswer
from exams.models import Exam, Section, Question

import logging

logger = logging.getLogger(__name__)


class AttemptResultsView(APIView):
    """
    Get detailed results for a completed exam attempt.
    
    GET /api/results/<attempt_id>/
    
    Returns:
    - Total score and percentage
    - Section-wise performance
    - Question-by-question review
    - Performance insights
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, attempt_id):
        """Get detailed results for an attempt."""
        
        # Get attempt and verify ownership
        attempt = get_object_or_404(Attempt, id=attempt_id)
        
        if attempt.user != request.user:
            return Response(
                {"error": "You don't have permission to view these results."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only show results for submitted/timeout attempts
        if attempt.status == 'in_progress':
            return Response(
                {"error": "Exam is still in progress. Complete the exam to see results."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exam = attempt.exam
        
        # Get all answers with optimized query (select_related to avoid N+1)
        answers = AttemptAnswer.objects.filter(attempt=attempt).select_related(
            'question', 'question__section'
        )
        
        # Calculate scores
        total_score = sum(answer.question.marks for answer in answers if answer.is_correct)
        total_marks = exam.total_marks
        percentage = (total_score / total_marks * 100) if total_marks > 0 else 0
        
        # Section-wise performance (optimized with prefetch_related)
        sections = Section.objects.filter(exam=exam).prefetch_related('questions')
        section_performance = []
        
        for section in sections:
            section_questions = section.questions.all()
            section_answers = answers.filter(question__section=section)
            
            section_score = sum(ans.question.marks for ans in section_answers if ans.is_correct)
            section_total = sum(q.marks for q in section_questions)
            section_accuracy = (section_score / section_total * 100) if section_total > 0 else 0
            
            answered_count = section_answers.filter(selected_option__isnull=False).count()
            
            section_performance.append({
                'section_name': section.name,
                'score': section_score,
                'total_marks': section_total,
                'accuracy': round(section_accuracy, 1),
                'answered': answered_count,
                'total_questions': section_questions.count(),
            })
        
        # Question-by-question review
        questions_review = []
        for answer in answers.order_by('question__section__order', 'question__question_number'):
            question = answer.question
            questions_review.append({
                'question_id': question.id,
                'question_number': question.question_number,
                'section_name': question.section.name,
                'question_text': question.question_text,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'option_d': question.option_d,
                'user_answer': answer.selected_option,
                'correct_answer': question.correct_option,
                'is_correct': answer.is_correct,
                'marks': question.marks,
            })
        
        # Performance insights
        strengths = [s['section_name'] for s in section_performance if s['accuracy'] >= 80]
        improvements = [s['section_name'] for s in section_performance if s['accuracy'] < 60]
        
        # Time analysis
        time_spent = None
        if attempt.finished_at and attempt.started_at:
            time_diff = attempt.finished_at - attempt.started_at
            hours = time_diff.seconds // 3600
            minutes = (time_diff.seconds % 3600) // 60
            time_spent = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        # Build response
        results_data = {
            'attempt_id': attempt.id,
            'exam_name': f"{exam.name} {exam.year}",
            'user': request.user.username,
            'started_at': attempt.started_at.isoformat(),
            'finished_at': attempt.finished_at.isoformat() if attempt.finished_at else None,
            'time_spent': time_spent,
            'status': attempt.status,
            'total_score': total_score,
            'total_marks': total_marks,
            'percentage': round(percentage, 2),
            'correct_answers': sum(1 for ans in answers if ans.is_correct),
            'total_questions': answers.count(),
            'section_performance': section_performance,
            'questions': questions_review,
            'insights': {
                'strengths': strengths,
                'improvements': improvements,
                'overall_performance': 'Excellent' if percentage >= 80 else 'Good' if percentage >= 60 else 'Needs Improvement',
            },
            # Video solution (only for completed exams)
            'solution_video_url': exam.solution_video_url if exam.solution_video_url else None,
        }
        
        logger.info(f"Results retrieved for attempt {attempt_id} by user {request.user.id}")
        
        return Response(results_data, status=status.HTTP_200_OK)


class UserDashboardView(APIView):
    """
    Get user dashboard data including stats, available exams, and past attempts.
    
    GET /api/dashboard/
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get dashboard data for the logged-in user."""
        
        user = request.user
        
        # Get all user attempts
        attempts = Attempt.objects.filter(user=user).select_related('exam')
        
        # Calculate stats
        completed_attempts = attempts.filter(status__in=['submitted', 'timeout'])
        total_attempts = completed_attempts.count()
        
        avg_score = 0
        best_score = 0
        if total_attempts > 0:
            scores = [
                (attempt.score / attempt.exam.total_marks * 100) if attempt.exam.total_marks > 0 else 0
                for attempt in completed_attempts
            ]
            avg_score = sum(scores) / len(scores) if scores else 0
            best_score = max(scores) if scores else 0
        
        # Available exams
        available_exams = Exam.objects.filter(is_published=True).prefetch_related('sections')
        exams_list = []
        
        for exam in available_exams:
            total_questions = Question.objects.filter(section__exam=exam).count()
            sections_count = exam.sections.count()
            
            exams_list.append({
                'id': exam.id,
                'name': f"{exam.name} {exam.year}",
                'duration_minutes': exam.duration_minutes,
                'total_marks': exam.total_marks,
                'total_questions': total_questions,
                'sections_count': sections_count,
                'access_tier': exam.access_tier,
                'is_premium': exam.is_premium,
            })
        
        # Recent attempts (last 10)
        recent_attempts = completed_attempts.order_by('-started_at')[:10]
        attempts_list = []
        
        for attempt in recent_attempts:
            percentage = (attempt.score / attempt.exam.total_marks * 100) if attempt.exam.total_marks > 0 else 0
            attempts_list.append({
                'id': attempt.id,
                'exam_name': f"{attempt.exam.name} {attempt.exam.year}",
                'date': attempt.started_at.date().isoformat(),
                'score': attempt.score,
                'total_marks': attempt.exam.total_marks,
                'percentage': round(percentage, 2),
                'status': attempt.status,
            })
        
        # Performance trend (last 5 attempts)
        trend_attempts = completed_attempts.order_by('-started_at')[:5]
        performance_trend = []
        
        for attempt in reversed(list(trend_attempts)):
            percentage = (attempt.score / attempt.exam.total_marks * 100) if attempt.exam.total_marks > 0 else 0
            performance_trend.append({
                'date': attempt.started_at.date().isoformat(),
                'score': round(percentage, 1),
                'exam': f"{attempt.exam.name} {attempt.exam.year}",
            })
        
        # Build response
        from payments.models import Subscription
        from django.utils import timezone
        
        # Get active subscription
        active_sub = Subscription.objects.filter(
            user=user,
            status='active',
            end_date__gt=timezone.now()
        ).select_related('plan').first()
        
        dashboard_data = {
            'user': {
                'username': user.username,
                'email': user.email,
                'tier': user.current_tier,
                'is_pro': user.is_pro(),
            },
            'subscription': {
                'plan': active_sub.plan.name if active_sub else None,
                'subscription_end': active_sub.end_date.isoformat() if active_sub else None,
                'is_active': active_sub.is_active if active_sub else False,
                'days_remaining': active_sub.days_remaining if active_sub else 0,
            },
            'stats': {
                'total_attempts': total_attempts,
                'average_score': round(avg_score, 1),
                'best_score': round(best_score, 1),
            },
            'available_exams': exams_list,
            'recent_attempts': attempts_list,
            'performance_trend': performance_trend,
        }
        
        logger.info(f"Dashboard data retrieved for user {user.id}")
        
        return Response(dashboard_data, status=status.HTTP_200_OK)
