"""
Production-ready exam timer views using Redis.

These views handle:
1. Starting exams with automatic Redis timers
2. Checking remaining time
3. Submitting answers with validation
4. Submitting exams with auto-timeout detection

All timer logic uses Redis with TTL for automatic expiration.
MySQL stores all permanent exam attempt data.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction, models
from django.shortcuts import get_object_or_404

from exams.models import Exam, Question
from exams.serializers import QuestionResponseSerializer
from results.models import Attempt, AttemptAnswer
from .redis_utils import timer_manager
from .serializers import SubmitAnswerSerializer

import logging

logger = logging.getLogger(__name__)


class StartExamView(APIView):
    """
    Start an exam and create Redis timer.
    
    POST /api/exam/timer/start/<int:exam_id>/

    Flow:
    1. Validate user is authenticated
    2. Validate exam exists and is published
    3. Check if user already has an ongoing attempt
    4. Create ExamAttempt in MySQL with status="ongoing"
    5. Create Redis timer with TTL = exam.duration * 60
    6. Return attempt details and remaining time
    
    Request: POST with exam_id in URL
    
    Response:
    {
        "attempt_id": 123,
        "exam_id": 45,
        "exam_title": "Python Basics",
        "duration_minutes": 60,
        "remaining_seconds": 3600,
        "total_questions": 50,
        "total_marks": 100
    }
    
    Error Responses:
    - 400: Exam not published / Already have ongoing attempt
    - 404: Exam not found
    - 500: Redis connection failed
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, exam_id):
        """Start a new exam attempt with Redis timer."""
        
        # Validate exam exists and is published
        exam = get_object_or_404(Exam, id=exam_id)
        
        if not exam.is_published:
            return Response(
                {"error": "This exam is not published yet."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for existing ongoing attempt
        existing_attempt = Attempt.objects.filter(
            user=request.user,
            exam=exam,
            status='in_progress'
        ).first()
        
        if existing_attempt:
            # Check if timer still exists in Redis
            remaining = timer_manager.get_remaining_time(existing_attempt.id)
            
            if remaining > 0:
                # Timer still running, return existing attempt
                return Response(
                    {
                        "attempt_id": existing_attempt.id,
                        "exam_id": exam.id,
                        "exam_title": f"{exam.name} {exam.year}",
                        "duration_minutes": exam.duration_minutes,
                        "remaining_seconds": remaining,
                        "total_questions": Question.objects.filter(section__exam=exam).count(),
                        "total_marks": exam.total_marks,
                        "message": "Resuming existing exam attempt"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                # Timer expired, mark as timeout and allow new attempt
                existing_attempt.status = 'timeout'
                existing_attempt.completed_at = timezone.now()
                existing_attempt.save()
                logger.info(f"Marked expired attempt {existing_attempt.id} as timeout, allowing new attempt")
                # Continue to create new attempt below
        
        
        # Create new attempt in MySQL
        try:
            with transaction.atomic():
                # Calculate attempt number (get max attempt number for this user-exam combo)
                max_attempt = Attempt.objects.filter(
                    user=request.user,
                    exam=exam
                ).aggregate(models.Max('attempt_number'))['attempt_number__max']
                
                next_attempt_number = (max_attempt or 0) + 1
                
                attempt = Attempt.objects.create(
                    user=request.user,
                    exam=exam,
                    attempt_number=next_attempt_number,
                    status='in_progress'
                )
                
                # Calculate duration in seconds
                duration_seconds = exam.duration_minutes * 60
                
                # Create Redis timer with TTL
                timer_created = timer_manager.create_timer(
                    attempt_id=attempt.id,
                    duration_seconds=duration_seconds
                )
                
                if not timer_created:
                    # Rollback: delete attempt if Redis timer failed
                    attempt.delete()
                    logger.error(f"Failed to create Redis timer for attempt {attempt.id}")
                    return Response(
                        {"error": "Failed to start exam timer. Please try again."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Success! Return attempt details
                logger.info(f"Started exam {exam.id} for user {request.user.id}, attempt {attempt.id}")
                
                return Response(
                    {
                        "attempt_id": attempt.id,
                        "exam_id": exam.id,
                        "exam_title": f"{exam.name} {exam.year}",
                        "duration_minutes": exam.duration_minutes,
                        "remaining_seconds": duration_seconds,
                        "total_questions": Question.objects.filter(section__exam=exam).count(),
                        "total_marks": exam.total_marks,
                    },
                    status=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            logger.error(f"Error starting exam {exam_id} for user {request.user.id}: {str(e)}")
            return Response(
                {"error": "An error occurred while starting the exam."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetRemainingTimeView(APIView):
    """
    Get remaining time for an exam attempt.
    
    GET /api/exam/remaining/<attempt_id>/
    
    Flow:
    1. Check Redis for TTL of timer key
    2. If TTL == -2 (key missing):
       - Update MySQL: attempt.status = "timeout"
       - Return status="timeout", remaining=0
    3. Else:
       - Return status="running", remaining=TTL
    
    Response (Running):
    {
        "status": "running",
        "remaining_seconds": 2847
    }
    
    Response (Timeout):
    {
        "status": "timeout",
        "remaining_seconds": 0,
        "message": "Exam time has expired"
    }
    
    Response (Completed):
    {
        "status": "completed",
        "remaining_seconds": 0,
        "message": "Exam already submitted"
    }
    
    Error Responses:
    - 403: Attempt does not belong to user
    - 404: Attempt not found
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, attempt_id):
        """Get remaining time for exam attempt."""
        
        # Get attempt and validate ownership
        attempt = get_object_or_404(Attempt, id=attempt_id)
        
        if attempt.user != request.user:
            return Response(
                {"error": "This exam attempt does not belong to you."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already completed
        if attempt.status == 'completed':
            return Response(
                {
                    "status": "completed",
                    "remaining_seconds": 0,
                    "message": "Exam already submitted"
                },
                status=status.HTTP_200_OK
            )
        
        # Get remaining time from Redis
        remaining = timer_manager.get_remaining_time(attempt_id)
        
        if remaining == -2:
            # Timer expired or missing
            if attempt.status == 'in_progress':
                # Update to timeout in MySQL
                attempt.status = 'timeout'
                attempt.finished_at = timezone.now()
                attempt.save()
                logger.info(f"Attempt {attempt_id} timed out")
            
            return Response(
                {
                    "status": "timeout",
                    "remaining_seconds": 0,
                    "message": "Exam time has expired"
                },
                status=status.HTTP_200_OK
            )
        
        elif remaining == -1:
            # Key exists but has no TTL (should never happen)
            logger.error(f"Timer for attempt {attempt_id} has no TTL - data corruption")
            return Response(
                {"error": "Timer configuration error. Please contact support."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        else:
            # Timer still running
            return Response(
                {
                    "status": "running",
                    "remaining_seconds": remaining
                },
                status=status.HTTP_200_OK
            )


class SubmitAnswerView(APIView):
    """
    Submit or update an answer to a question.
    
    POST /api/exam/submit-answer/
    
    Request Body:
    {
        "attempt_id": 123,
        "question_id": 456,
        "selected_option": "B"
    }
    
    Flow:
    1. Validate attempt belongs to user
    2. Validate attempt is ongoing (not completed/timeout)
    3. Check Redis timer - if expired, reject
    4. Update or create answer in MySQL
    5. Return success
    
    Response:
    {
        "status": "saved",
        "question_id": 456,
        "selected_option": "B"
    }
    
    Error Responses:
    - 400: Exam already completed / Invalid option
    - 403: Attempt does not belong to user
    - 404: Attempt or question not found
    - 410: Exam time expired
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Submit an answer to a question."""
        
        # Validate request data
        serializer = SubmitAnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attempt_id = serializer.validated_data['attempt_id']
        question_id = serializer.validated_data['question_id']
        selected_option = serializer.validated_data['selected_option']
        
        # Get attempt and validate ownership
        attempt = get_object_or_404(Attempt, id=attempt_id)
        
        if attempt.user != request.user:
            return Response(
                {"error": "This exam attempt does not belong to you."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already completed
        if attempt.status == 'submitted':
            return Response(
                {"error": "Exam already submitted. Cannot modify answers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check Redis timer
        remaining = timer_manager.get_remaining_time(attempt_id)
        
        if remaining == -2:
            # Timer expired
            if attempt.status == 'in_progress':
                attempt.status = 'timeout'
                attempt.finished_at = timezone.now()
                attempt.save()
            
            return Response(
                {"error": "Exam time has expired. Cannot submit answers."},
                status=status.HTTP_410_GONE
            )
        
        # Validate question belongs to this exam
        question = get_object_or_404(Question, id=question_id)
        
        if question.section.exam_id != attempt.exam_id:
            return Response(
                {"error": "This question does not belong to this exam."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save or update answer
        try:
            answer, created = AttemptAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={
                    'selected_option': selected_option,
                }
            )
            
            action = "saved" if created else "updated"
            logger.info(f"Answer {action} for attempt {attempt_id}, question {question_id}")
            
            return Response(
                {
                    "status": "saved",
                    "question_id": question_id,
                    "selected_option": selected_option,
                    "action": action
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error saving answer for attempt {attempt_id}, question {question_id}: {str(e)}")
            return Response(
                {"error": "Failed to save answer. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SubmitExamView(APIView):
    """
    Submit an exam and calculate score.
    
    POST /api/exam/submit/<attempt_id>/
    
    Flow:
    1. Validate attempt belongs to user
    2. Check if already submitted
    3. Check Redis timer:
       - If missing (expired) → status="timeout"
       - If exists → delete timer, status="submitted"
    4. Calculate score by comparing answers
    5. Update MySQL: score, status, completed_at
    6. Return results
    
    Response:
    {
        "status": "submitted",
        "score": 75,
        "total_marks": 100,
        "percentage": 75.0,
        "correct_answers": 15,
        "total_questions": 20,
        "time_taken_minutes": 45
    }
    
    Error Responses:
    - 403: Attempt does not belong to user
    - 404: Attempt not found
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, attempt_id):
        """Submit exam and calculate score."""
        
        # Get attempt and validate ownership
        attempt = get_object_or_404(Attempt, id=attempt_id)
        
        if attempt.user != request.user:
            return Response(
                {"error": "This exam attempt does not belong to you."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already submitted
        if attempt.status == 'submitted':
            return Response(
                {
                    "status": "already_completed",
                    "score": attempt.score or 0,
                    "total_marks": attempt.exam.total_marks,
                    "percentage": round((attempt.score or 0) / attempt.exam.total_marks * 100, 2),
                    "message": "Exam was already submitted"
                },
                status=status.HTTP_200_OK
            )
        
        # Check Redis timer
        remaining = timer_manager.get_remaining_time(attempt_id)
        
        if remaining == -2:
            # Timer expired - mark as timeout
            submission_status = 'timeout'
            logger.info(f"Attempt {attempt_id} submitted after timeout")
        else:
            # Timer still running - normal submission
            # Delete timer from Redis
            timer_manager.delete_timer(attempt_id)
            submission_status = 'submitted'
            logger.info(f"Attempt {attempt_id} submitted with {remaining}s remaining")
        
        # Calculate score
        try:
            with transaction.atomic():
                score = 0
                correct_count = 0
                total_questions = Question.objects.filter(section__exam=attempt.exam).count()
                
                # Get all answers for this attempt
                answers = AttemptAnswer.objects.filter(attempt=attempt).select_related('question')
                
                for answer in answers:
                    if answer.is_correct:
                        score += answer.question.marks
                        correct_count += 1
                
                # Calculate time taken
                time_taken = None
                if attempt.started_at:
                    time_delta = timezone.now() - attempt.started_at
                    time_taken = int(time_delta.total_seconds() / 60)  # Convert to minutes
                
                # Update attempt
                attempt.score = score
                attempt.status = 'submitted'
                attempt.finished_at = timezone.now()
                attempt.save()
                
                # Calculate percentage
                percentage = round((score / attempt.exam.total_marks * 100), 2) if attempt.exam.total_marks > 0 else 0
                
                logger.info(f"Exam submitted - Attempt {attempt_id}, Score: {score}/{attempt.exam.total_marks}")
                
                response_data = {
                    "status": submission_status,
                    "score": score,
                    "total_marks": attempt.exam.total_marks,
                    "percentage": percentage,
                    "correct_answers": correct_count,
                    "total_questions": total_questions,
                }
                
                if time_taken is not None:
                    response_data["time_taken_minutes"] = time_taken
                
                if submission_status == 'timeout':
                    response_data["message"] = "Exam submitted after time expired"
                
                return Response(response_data, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Error submitting exam {attempt_id}: {str(e)}")
            return Response(
                {"error": "Failed to submit exam. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetExamQuestionsView(APIView):
    """
    Get all questions for an exam attempt.
    
    GET /api/exam/questions/<attempt_id>/
    
    Returns all questions without revealing correct answers.
    Used by frontend to display exam questions.
    
    Response:
    {
        "attempt_id": 123,
        "exam_title": "Python Basics",
        "questions": [
            {
                "id": 1,
                "text": "What is Python?",
                "option_a": "A snake",
                "option_b": "A programming language",
                "option_c": "A framework",
                "option_d": "A database",
                "marks": 2
            },
            ...
        ]
    }
    
    Error Responses:
    - 403: Attempt does not belong to user
    - 404: Attempt not found
    - 410: Exam time expired
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, attempt_id):
        """Get all questions for exam attempt with Redis caching."""
        from django.core.cache import cache
        
        # Get attempt with exam in one query (optimization)
        attempt = get_object_or_404(
            Attempt.objects.select_related('exam'), 
            id=attempt_id
        )
        
        if attempt.user != request.user:
            return Response(
                {"error": "This exam attempt does not belong to you."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if timer expired
        if attempt.status == 'in_progress':
            remaining = timer_manager.get_remaining_time(attempt_id)
            if remaining == -2:
                attempt.status = 'timeout'
                attempt.finished_at = timezone.now()
                attempt.save()
                
                return Response(
                    {"error": "Exam time has expired."},
                    status=status.HTTP_410_GONE
                )
        
        # Try to get questions from Redis cache first
        exam_id = attempt.exam.id
        cache_key = f'exam_{exam_id}_questions'
        questions_data = cache.get(cache_key)
        
        if not questions_data:
            # Cache miss - fetch from database with optimizations
            logger.info(f"Cache miss for exam {exam_id}, fetching from DB")
            
            # Optimized query: select_related to avoid N+1, values() for speed
            questions_data = list(
                Question.objects.filter(section__exam=attempt.exam)
                .select_related('section')
                .values(
                    'id', 'question_text', 'option_a', 'option_b',
                    'option_c', 'option_d', 'marks', 'question_number',
                    'section__name', 'section__order'
                )
                .order_by('section__order', 'question_number')
            )
            
            # Rename fields for frontend compatibility
            for q in questions_data:
                q['text'] = q.pop('question_text')  # Frontend expects 'text'
                q['section_name'] = q.pop('section__name')
                q['section_order'] = q.pop('section__order')
            
            # Cache for 1 hour (questions rarely change)
            cache.set(cache_key, questions_data, 3600)
            logger.info(f"Cached {len(questions_data)} questions for exam {exam_id}")
        else:
            logger.info(f"Cache hit for exam {exam_id}, serving from Redis")
            # Also rename fields from cache (in case cache has old format)
            for q in questions_data:
                if 'question_text' in q and 'text' not in q:
                    q['text'] = q.pop('question_text')
                if 'section__name' in q and 'section_name' not in q:
                    q['section_name'] = q.pop('section__name')
                if 'section__order' in q and 'section_order' not in q:
                    q['section_order'] = q.pop('section__order')
        
        # Get user's saved answers (optimized with values_list)
        saved_answers = dict(
            AttemptAnswer.objects.filter(attempt=attempt)
            .values_list('question_id', 'selected_option')
        )
        
        return Response(
            {
                "attempt_id": attempt_id,
                "exam_title": f"{attempt.exam.name} {attempt.exam.year}",
                "questions": questions_data,
                "saved_answers": saved_answers
            },
            status=status.HTTP_200_OK
        )
