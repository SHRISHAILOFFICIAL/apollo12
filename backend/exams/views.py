from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count

from .models import Exam, Section, Question
from .serializers import (
    ExamSerializer, ExamListSerializer, ExamDetailSerializer,
    SectionSerializer, SectionWithQuestionsSerializer,
    QuestionSerializer, QuestionListSerializer
)


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
        queryset = Exam.objects.all()
        # Non-admin users only see published exams
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset.order_by('-year', 'name')
    
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        """Get all sections for an exam"""
        exam = self.get_object()
        sections = exam.sections.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get all questions for an exam"""
        exam = self.get_object()
        questions = Question.objects.filter(section__exam=exam).order_by('section__order', 'question_number')
        serializer = QuestionListSerializer(questions, many=True)
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
