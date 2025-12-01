from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q

from .models import ExamAttempt, AttemptResponse
from exams.models import Exam, Question
from .serializers import (
    ExamAttemptSerializer, ExamAttemptDetailSerializer,
    ExamAttemptStartSerializer, ExamAttemptSubmitSerializer,
    AttemptResponseSerializer, AttemptResponseCreateSerializer,
    ExamResultSerializer
)


class ExamAttemptViewSet(viewsets.ModelViewSet):
    """ViewSet for managing exam attempts"""
    
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return attempts for current user only (students) or all (admins)"""
        user = self.request.user
        if user.role == 'admin':
            return ExamAttempt.objects.all()
        return ExamAttempt.objects.filter(user=user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ExamAttemptDetailSerializer
        elif self.action == 'start_exam':
            return ExamAttemptStartSerializer
        elif self.action == 'submit_exam':
            return ExamAttemptSubmitSerializer
        return ExamAttemptSerializer
    
    @action(detail=False, methods=['post'])
    def start_exam(self, request):
        """
        Start a new exam attempt
        POST /api/attempts/start_exam/
        Body: {exam_id}
        """
        serializer = ExamAttemptStartSerializer(data=request.data)
        if serializer.is_valid():
            exam_id = serializer.validated_data['exam_id']
            exam = Exam.objects.get(id=exam_id)
            
            # Check if user has an ongoing attempt
            ongoing_attempt = ExamAttempt.objects.filter(
                user=request.user,
                exam=exam,
                status='in_progress'
            ).first()
            
            if ongoing_attempt:
                return Response({
                    'message': 'You have an ongoing attempt for this exam',
                    'attempt': ExamAttemptDetailSerializer(ongoing_attempt).data
                }, status=status.HTTP_200_OK)
            
            # Create new attempt
            attempt = ExamAttempt.objects.create(
                user=request.user,
                exam=exam,
                status='in_progress'
            )
            
            # Create empty responses for all questions
            questions = exam.questions.all()
            for question in questions:
                AttemptResponse.objects.create(
                    attempt=attempt,
                    question=question
                )
            
            return Response({
                'message': 'Exam started successfully',
                'attempt': ExamAttemptDetailSerializer(attempt).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """
        Submit answer for a question
        POST /api/attempts/{id}/submit_answer/
        Body: {question_id, selected_option_id}
        """
        attempt = self.get_object()
        
        if attempt.status != 'in_progress':
            return Response({
                'error': 'This attempt is already completed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        question_id = request.data.get('question_id')
        selected_option_id = request.data.get('selected_option_id')
        
        if not question_id:
            return Response({
                'error': 'question_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = AttemptResponse.objects.get(
                attempt=attempt,
                question_id=question_id
            )
            
            # Update selected option
            response.selected_option_id = selected_option_id
            
            # Check if answer is correct
            if selected_option_id:
                response.is_correct = response.question.options.filter(
                    id=selected_option_id,
                    is_correct=True
                ).exists()
            else:
                response.is_correct = None
            
            response.save()
            
            return Response({
                'message': 'Answer submitted successfully',
                'response': AttemptResponseSerializer(response).data
            })
        
        except AttemptResponse.DoesNotExist:
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
        
        # Calculate score
        correct_answers = attempt.responses.filter(is_correct=True).count()
        total_marks = sum([
            response.question.marks 
            for response in attempt.responses.filter(is_correct=True)
        ])
        
        # Update attempt
        attempt.end_time = timezone.now()
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
        attempts = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """
        Get ongoing attempts for current user
        GET /api/attempts/in_progress/
        """
        attempts = self.get_queryset().filter(
            user=request.user,
            status='in_progress'
        )
        serializer = ExamAttemptDetailSerializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Get completed attempts for current user
        GET /api/attempts/completed/
        """
        attempts = self.get_queryset().filter(
            user=request.user,
            status__in=['submitted', 'timeout']
        )
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


class AttemptResponseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing attempt responses"""
    
    queryset = AttemptResponse.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return AttemptResponseCreateSerializer
        return AttemptResponseSerializer
    
    def get_queryset(self):
        """Filter responses by attempt if provided"""
        queryset = AttemptResponse.objects.all()
        attempt_id = self.request.query_params.get('attempt_id')
        
        if attempt_id:
            queryset = queryset.filter(attempt_id=attempt_id)
        
        # Students can only see their own responses
        if self.request.user.role != 'admin':
            queryset = queryset.filter(attempt__user=self.request.user)
        
        return queryset
