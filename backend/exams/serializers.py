from rest_framework import serializers
from .models import Exam, Section, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""
    
    class Meta:
        model = Question
        fields = [
            'id', 'section', 'question_number', 'question_text', 'plain_text',
            'option_a', 'option_b', 'option_c', 'option_d', 'correct_option',
            'marks', 'diagram_url', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class QuestionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing questions (without correct answer)"""
    text = serializers.CharField(source='question_text', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    section_order = serializers.IntegerField(source='section.order', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_number', 'text', 'question_text', 'plain_text',
            'option_a', 'option_b', 'option_c', 'option_d',
            'marks', 'diagram_url', 'section_name', 'section_order'
        ]


# Alias for backward compatibility
QuestionResponseSerializer = QuestionListSerializer


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for Section model"""
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = ['id', 'exam', 'name', 'order', 'max_marks', 'question_count']
        read_only_fields = ['id']
    
    def get_question_count(self, obj):
        return obj.questions.count()


class SectionWithQuestionsSerializer(serializers.ModelSerializer):
    """Section serializer with nested questions"""
    questions = QuestionListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Section
        fields = ['id', 'name', 'order', 'max_marks', 'questions']


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for Exam model"""
    section_count = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()
    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'year', 'title', 'description', 'total_marks', 'duration_minutes',
            'is_published', 'section_count', 'question_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_section_count(self, obj):
        return obj.sections.count()
    
    def get_question_count(self, obj):
        return Question.objects.filter(section__exam=obj).count()


class ExamListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing exams"""
    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    
    class Meta:
        model = Exam
        fields = ['id', 'name', 'year', 'title', 'description', 'total_marks', 'duration_minutes', 'is_published']


class ExamDetailSerializer(serializers.ModelSerializer):
    """Detailed exam serializer with sections and questions"""
    sections = SectionWithQuestionsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'year', 'total_marks', 'duration_minutes',
            'is_published', 'sections', 'created_at', 'updated_at'
        ]
