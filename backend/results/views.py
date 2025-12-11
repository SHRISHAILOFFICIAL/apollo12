from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q

from .models import Attempt, AttemptAnswer
from exams.models import Exam, Question
from .serializers import (
    AttemptSerializer, AttemptDetailSerializer,
    AttemptStartSerializer, AttemptSubmitSerializer,
    AttemptAnswerSerializer, AttemptAnswerCreateSerializer,
    ExamResultSerializer
)


class AttemptViewSet(viewsets.ModelViewSet):
    """ViewSet for managing exam attempts"""
    
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return attempts for current user with optimized queries"""
        return Attempt.objects.filter(user=self.request.user).select_related(
            'user', 'exam'
        ).prefetch_related(
            'answers__question__section'
        )
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return AttemptDetailSerializer
        elif self.action == 'start_exam':
            return AttemptStartSerializer
        elif self.action == 'submit_exam':
            return AttemptSubmitSerializer
        return AttemptSerializer
    
    @action(detail=False, methods=['post'])
    def start_exam(self, request):
        """
        Start a new exam attempt
        POST /api/attempts/start_exam/
        Body: {exam_id}
        """
        serializer = AttemptStartSerializer(data=request.data)
        if serializer.is_valid():
            exam_id = serializer.validated_data['exam_id']
            exam = Exam.objects.get(id=exam_id)
            
            # Check if user has an ongoing attempt
            ongoing_attempt = Attempt.objects.filter(
                user=request.user,
                exam=exam,
                status='in_progress'
            ).first()
            
            if ongoing_attempt:
                return Response({
                    'message': 'You have an ongoing attempt for this exam',
                    'attempt': AttemptDetailSerializer(ongoing_attempt).data
                }, status=status.HTTP_200_OK)
            
            # Create new attempt
            attempt = Attempt.objects.create(
                user=request.user,
                exam=exam,
                status='in_progress'
            )
            
            # Create empty answers for all questions (optimized bulk create)
            questions = Question.objects.filter(section__exam=exam).select_related('section')
            answers_to_create = [
                AttemptAnswer(attempt=attempt, question=question)
                for question in questions
            ]
            AttemptAnswer.objects.bulk_create(answers_to_create)
            
            return Response({
                'message': 'Exam started successfully',
                'attempt': AttemptDetailSerializer(attempt).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """
        Submit answer for a question
        POST /api/attempts/{id}/submit_answer/
        Body: {question_id, selected_option} (A/B/C/D)
        """
        attempt = self.get_object()
        
        if attempt.status != 'in_progress':
            return Response({
                'error': 'This attempt is already completed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        question_id = request.data.get('question_id')
        selected_option = request.data.get('selected_option')
        
        if not question_id:
            return Response({
                'error': 'question_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if selected_option and selected_option not in ['A', 'B', 'C', 'D']:
            return Response({
                'error': 'selected_option must be A, B, C, or D'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            answer = AttemptAnswer.objects.get(
                attempt=attempt,
                question_id=question_id
            )
            
            # Update selected option
            answer.selected_option = selected_option
            
            # Check if answer is correct
            if selected_option:
                answer.is_correct = (selected_option == answer.question.correct_option)
            else:
                answer.is_correct = False
            
            answer.save()
            
            return Response({
                'message': 'Answer submitted successfully',
                'answer': AttemptAnswerSerializer(answer).data
            })
        
        except AttemptAnswer.DoesNotExist:
            return Response({
                'error': 'Question not found in this attempt'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def submit_exam(self, request, pk=None):
        """
        Submit the entire exam
        POST /api/attempts/{id}/submit_exam/
        """
        attempt = self.get_object()
        
        if attempt.user != request.user:
            return Response({
                'error': 'This attempt does not belong to you'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if attempt.status != 'in_progress':
            return Response({
                'error': 'This attempt is already completed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate score (optimized query)
        correct_answers = attempt.answers.filter(is_correct=True).select_related('question')
        total_marks = sum(answer.question.marks for answer in correct_answers)
        
        # Update attempt
        attempt.finished_at = timezone.now()
        attempt.score = total_marks
        attempt.status = 'submitted'
        attempt.save()
        
        return Response({
            'message': 'Exam submitted successfully',
            'result': ExamResultSerializer(attempt).data
        })
    
    @action(detail=False, methods=['get'])
    def my_attempts(self, request):
        """
        Get all attempts for current user
        GET /api/attempts/my_attempts/
        """
        attempts = self.get_queryset()
        serializer = self.get_serializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """
        Get ongoing attempts for current user
        GET /api/attempts/in_progress/
        """
        attempts = self.get_queryset().filter(status='in_progress')
        serializer = AttemptDetailSerializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Get completed attempts for current user
        GET /api/attempts/completed/
        """
        attempts = self.get_queryset().filter(status__in=['submitted', 'timeout'])
        serializer = self.get_serializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        """
        Get detailed result for an attempt
        GET /api/attempts/{id}/result/
        """
        attempt = self.get_object()
        
        if attempt.status == 'in_progress':
            return Response({
                'error': 'Exam is still in progress'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExamResultSerializer(attempt)
        return Response(serializer.data)


class AttemptAnswerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing attempt answers"""
    
    queryset = AttemptAnswer.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return AttemptAnswerCreateSerializer
        return AttemptAnswerSerializer
    
    def get_queryset(self):
        """Filter answers by attempt if provided (optimized)"""
        queryset = AttemptAnswer.objects.select_related(
            'attempt__user', 'attempt__exam', 'question__section'
        )
        attempt_id = self.request.query_params.get('attempt_id')
        
        if attempt_id:
            queryset = queryset.filter(attempt_id=attempt_id)
        
        # Students can only see their own answers
        queryset = queryset.filter(attempt__user=self.request.user)
        
        return queryset
