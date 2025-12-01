from rest_framework import serializers
from .models import Subject, Exam, ExamSubject, Question, Option


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class OptionSerializer(serializers.ModelSerializer):
    """Serializer for Option model"""
    
    class Meta:
        model = Option
        fields = ['id', 'question', 'option_text', 'is_correct']
        read_only_fields = ['id']


class OptionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating options (without question FK in payload)"""
    
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model with options"""
    
    options = OptionSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'exam', 'subject', 'subject_name', 'question_text',
            'marks', 'difficulty', 'created_at', 'options'
        ]
        read_only_fields = ['id', 'created_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating questions with options"""
    
    options = OptionCreateSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = ['id', 'exam', 'subject', 'question_text', 'marks', 'difficulty', 'options']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Create question with options"""
        options_data = validated_data.pop('options', [])
        question = Question.objects.create(**validated_data)
        
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        
        return question


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Detailed question serializer for exam-taking (without correct answers)"""
    
    options = serializers.SerializerMethodField()
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'subject', 'subject_name', 'question_text',
            'marks', 'difficulty', 'options'
        ]
    
    def get_options(self, obj):
        """Return options without is_correct field for students"""
        options = obj.options.all()
        return [{'id': opt.id, 'option_text': opt.option_text} for opt in options]


class ExamSubjectSerializer(serializers.ModelSerializer):
    """Serializer for ExamSubject mapping"""
    
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = ExamSubject
        fields = ['id', 'exam', 'subject', 'subject_name']
        read_only_fields = ['id']


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for Exam model"""
    
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True, source='exam_subjects.subject')
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'description', 'duration_minutes', 'total_marks',
            'is_published', 'created_by', 'created_by_name', 'created_at',
            'updated_at', 'subjects', 'questions_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class ExamListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing exams"""
    
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'description', 'duration_minutes',
            'total_marks', 'is_published', 'questions_count'
        ]
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class ExamDetailSerializer(serializers.ModelSerializer):
    """Detailed exam serializer with all questions"""
    
    questions = QuestionSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True, source='exam_subjects.subject')
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'description', 'duration_minutes', 'total_marks',
            'is_published', 'created_by', 'created_by_name', 'created_at',
            'updated_at', 'subjects', 'questions'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExamTakingSerializer(serializers.ModelSerializer):
    """Serializer for students taking an exam (questions without answers)"""
    
    questions = QuestionDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'duration_minutes', 'total_marks', 'questions']
        read_only_fields = ['id']
