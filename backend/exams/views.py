from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Exam, Section, Question
from .serializers import (
    ExamSerializer, ExamListSerializer, ExamDetailSerializer,
    SectionSerializer, SectionWithQuestionsSerializer,
    QuestionSerializer, QuestionListSerializer
)
from utils.cache import cache_response, get_cached_exam, cache_exam_data
from .permissions import can_access_exam


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet for Exam CRUD operations"""
    
    queryset = Exam.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExamListSerializer
        elif self.action == 'retrieve':
            return ExamDetailSerializer
        return ExamSerializer
    
    def get_queryset(self):
        # Optimize with select_related for better performance
        queryset = Exam.objects.all().prefetch_related('sections')
        # Non-admin users only see published exams
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset.order_by('-year', 'name')
    
    @method_decorator(cache_page(3600))  # Cache for 1 hour
    def list(self, request, *args, **kwargs):
        """Cached exam list"""
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Cached exam detail with questions - with access control"""
        exam = self.get_object()
        
        # Check if user has access to this exam
        can_access, reason = can_access_exam(request.user, exam)
        if not can_access:
            return Response({
                'success': False,
                'error': reason,
                'requires_pro': exam.is_premium,
                'exam_id': exam.id,
                'exam_name': exam.name
            }, status=status.HTTP_403_FORBIDDEN)
        
        exam_id = kwargs.get('pk')
        cache_key = f"apollo11:exam:{exam_id}:detail"
        
        # Try cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Get from database with optimized query
        response = super().retrieve(request, *args, **kwargs)
        
        # Cache successful response for 1 hour
        if response.status_code == 200:
            cache.set(cache_key, response.data, 3600)
        
        return response
    
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        """Get all sections for an exam"""
        exam = self.get_object()
        sections = exam.sections.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get all questions for an exam (cached) - with access control"""
        exam = self.get_object()
        
        # Check if user has access to this exam
        can_access, reason = can_access_exam(request.user, exam)
        if not can_access:
            return Response({
                'success': False,
                'error': reason,
                'requires_pro': exam.is_premium
            }, status=status.HTTP_403_FORBIDDEN)
        
        cache_key = f"apollo11:exam:{pk}:questions"
        
        # Try cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Optimize query with select_related
        questions = Question.objects.filter(section__exam=exam).select_related('section').order_by('section__order', 'question_number')
        serializer = QuestionListSerializer(questions, many=True)
        
        # Cache for 1 hour
        cache.set(cache_key, serializer.data, 3600)
        
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    """ViewSet for Section CRUD operations"""
    
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    
    def get_queryset(self):
        queryset = Section.objects.all()
        exam_id = self.request.query_params.get('exam', None)
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        return queryset.order_by('exam', 'order')
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get all questions for a section"""
        section = self.get_object()
        questions = section.questions.all()
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for Question CRUD operations"""
    
    queryset = Question.objects.all()
    
    def get_serializer_class(self):
        # Admin users get full serializer with correct answers
        if self.request.user.is_staff:
            return QuestionSerializer
        return QuestionListSerializer
    
    def get_queryset(self):
        queryset = Question.objects.all()
        section_id = self.request.query_params.get('section', None)
        exam_id = self.request.query_params.get('exam', None)
        
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        elif exam_id:
            queryset = queryset.filter(section__exam_id=exam_id)
        
        return queryset.order_by('section__order', 'question_number')
