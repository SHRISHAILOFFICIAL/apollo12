from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q, Count

from .models import Subject, Exam, ExamSubject, Question, Option
from .serializers import (
    SubjectSerializer, ExamSerializer, ExamListSerializer,
    ExamDetailSerializer, ExamTakingSerializer,
    QuestionSerializer, QuestionCreateSerializer,
    OptionSerializer, ExamSubjectSerializer
)


class SubjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing subjects"""
    
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def exams(self, request, pk=None):
        """
        Get all exams for a subject
        GET /api/subjects/{id}/exams/
        """
        subject = self.get_object()
        exams = Exam.objects.filter(exam_subjects__subject=subject, is_published=True)
        serializer = ExamListSerializer(exams, many=True)
        return Response(serializer.data)


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet for managing exams"""
    
    queryset = Exam.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ExamListSerializer
        elif self.action == 'retrieve':
            return ExamDetailSerializer
        elif self.action == 'take_exam':
            return ExamTakingSerializer
        return ExamSerializer
    
    def get_queryset(self):
        """Filter exams based on user role"""
        user = self.request.user
        
        if user.is_authenticated and user.role == 'admin':
            # Admins can see all exams
            return Exam.objects.all()
        else:
            # Students can only see published exams
            return Exam.objects.filter(is_published=True)
    
    def perform_create(self, serializer):
        """Set current user as creator"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        Get all published exams
        GET /api/exams/published/
        """
        exams = Exam.objects.filter(is_published=True).annotate(
            questions_count=Count('questions')
        )
        serializer = ExamListSerializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def take_exam(self, request, pk=None):
        """
        Get exam with questions for taking (hides correct answers)
        GET /api/exams/{id}/take_exam/
        """
        exam = self.get_object()
        
        if not exam.is_published:
            return Response({
                'error': 'This exam is not published yet'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ExamTakingSerializer(exam)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """
        Publish an exam (admin only)
        POST /api/exams/{id}/publish/
        """
        if request.user.role != 'admin':
            return Response({
                'error': 'Only admins can publish exams'
            }, status=status.HTTP_403_FORBIDDEN)
        
        exam = self.get_object()
        exam.is_published = True
        exam.save()
        
        return Response({
            'message': 'Exam published successfully',
            'exam': ExamSerializer(exam).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        """
        Unpublish an exam (admin only)
        POST /api/exams/{id}/unpublish/
        """
        if request.user.role != 'admin':
            return Response({
                'error': 'Only admins can unpublish exams'
            }, status=status.HTTP_403_FORBIDDEN)
        
        exam = self.get_object()
        exam.is_published = False
        exam.save()
        
        return Response({
            'message': 'Exam unpublished successfully',
            'exam': ExamSerializer(exam).data
        })
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Get exam statistics
        GET /api/exams/{id}/statistics/
        """
        exam = self.get_object()
        
        stats = {
            'total_questions': exam.questions.count(),
            'total_marks': exam.total_marks,
            'duration_minutes': exam.duration_minutes,
            'subjects': exam.exam_subjects.count(),
            'attempts_count': exam.attempts.count(),
            'completed_attempts': exam.attempts.filter(status='submitted').count(),
        }
        
        return Response(stats)


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing questions"""
    
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionCreateSerializer
        return QuestionSerializer
    
    def get_queryset(self):
        """Filter questions by exam if provided"""
        queryset = Question.objects.all()
        exam_id = self.request.query_params.get('exam_id')
        subject_id = self.request.query_params.get('subject_id')
        
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_option(self, request, pk=None):
        """
        Add an option to a question
        POST /api/questions/{id}/add_option/
        Body: {option_text, is_correct}
        """
        question = self.get_object()
        
        option_data = request.data.copy()
        option_data['question'] = question.id
        
        serializer = OptionSerializer(data=option_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Option added successfully',
                'option': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OptionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing options"""
    
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter options by question if provided"""
        queryset = Option.objects.all()
        question_id = self.request.query_params.get('question_id')
        
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        
        return queryset
