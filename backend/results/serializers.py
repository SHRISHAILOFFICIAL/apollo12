from rest_framework import serializers
from .models import Attempt, AttemptAnswer
from exams.models import Question, Exam
from users.models import User


class AttemptAnswerSerializer(serializers.ModelSerializer):
    """Serializer for individual question answers"""
    
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question_number = serializers.IntegerField(source='question.question_number', read_only=True)
    correct_option = serializers.SerializerMethodField()
    
    class Meta:
        model = AttemptAnswer
        fields = [
            'id', 'attempt', 'question', 'question_number', 'question_text',
            'selected_option', 'is_correct', 'correct_option'
        ]
        read_only_fields = ['id', 'is_correct']

    def get_correct_option(self, obj):
        """Return correct option only after attempt is submitted"""
        if obj.attempt.status in ['submitted', 'timeout']:
            return obj.question.correct_option
        return None


class AttemptAnswerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating answers during exam"""
    
    class Meta:
        model = AttemptAnswer
        fields = ['id', 'attempt', 'question', 'selected_option']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Create answer (is_correct computed automatically)"""
        answer = AttemptAnswer(**validated_data)
        answer.save()
        return answer
    
    def update(self, instance, validated_data):
        """Update answer (is_correct recomputed automatically)"""
        instance.selected_option = validated_data.get('selected_option', instance.selected_option)
        instance.save()
        return instance


class AttemptSerializer(serializers.ModelSerializer):
    """Serializer for exam attempts"""
    
    user_name = serializers.CharField(source='user.username', read_only=True)
    exam_name = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    duration_minutes = serializers.IntegerField(source='exam.duration_minutes', read_only=True)
    
    class Meta:
        model = Attempt
        fields = [
            'id', 'user', 'user_name', 'exam', 'exam_name',
            'started_at', 'finished_at', 'score', 'status',
            'answers_count', 'duration_minutes', 'randomized_order'
        ]
        read_only_fields = ['id', 'started_at', 'score']
    
    def get_exam_name(self, obj):
        return f"{obj.exam.name} {obj.exam.year}"
    
    def get_answers_count(self, obj):
        return obj.answers.count()


class AttemptDetailSerializer(serializers.ModelSerializer):
    """Detailed attempt with all answers"""
    
    answers = AttemptAnswerSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    exam_name = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    answered_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    
    class Meta:
        model = Attempt
        fields = [
            'id', 'user', 'user_name', 'exam', 'exam_name',
            'started_at', 'finished_at', 'score', 'status',
            'total_questions', 'answered_questions', 'correct_answers',
            'randomized_order', 'answers'
        ]
        read_only_fields = ['id', 'started_at']
    
    def get_exam_name(self, obj):
        return f"{obj.exam.name} {obj.exam.year}"
    
    def get_total_questions(self, obj):
        return Question.objects.filter(section__exam=obj.exam).count()
    
    def get_answered_questions(self, obj):
        return obj.answers.filter(selected_option__isnull=False).count()
    
    def get_correct_answers(self, obj):
        # Count answers where selected_option matches correct_option
        from django.db.models import F
        return obj.answers.filter(selected_option=F('question__correct_option')).count()


class AttemptStartSerializer(serializers.Serializer):
    """Serializer for starting an exam"""
    
    exam_id = serializers.IntegerField()
    
    def validate_exam_id(self, value):
        """Validate exam exists and is published"""
        try:
            exam = Exam.objects.get(id=value)
            if not exam.is_published:
                raise serializers.ValidationError("This exam is not published yet")
            return value
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Exam not found")


class AttemptSubmitSerializer(serializers.Serializer):
    """Serializer for submitting an exam"""
    
    attempt_id = serializers.IntegerField()
    
    def validate_attempt_id(self, value):
        """Validate attempt exists and belongs to user"""
        user = self.context.get('user')
        try:
            attempt = Attempt.objects.get(id=value, user=user)
            if attempt.status != 'in_progress':
                raise serializers.ValidationError("This attempt is already completed")
            return value
        except Attempt.DoesNotExist:
            raise serializers.ValidationError("Attempt not found")


class ExamResultSerializer(serializers.ModelSerializer):
    """Serializer for exam results/summary"""
    
    user_name = serializers.CharField(source='user.username', read_only=True)
    exam_name = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    wrong_answers = serializers.SerializerMethodField()
    unanswered = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Attempt
        fields = [
            'id', 'user_name', 'exam_name', 'started_at', 'finished_at',
            'score', 'total_questions', 'correct_answers', 'wrong_answers',
            'unanswered', 'percentage', 'status'
        ]
    
    def get_exam_name(self, obj):
        return f"{obj.exam.name} {obj.exam.year}"
    
    def get_total_questions(self, obj):
        return Question.objects.filter(section__exam=obj.exam).count()
    
    def get_correct_answers(self, obj):
        from django.db.models import F
        return obj.answers.filter(selected_option=F('question__correct_option')).count()
    
    def get_wrong_answers(self, obj):
        from django.db.models import F, Q
        return obj.answers.filter(
            ~Q(selected_option=F('question__correct_option')),
            selected_option__isnull=False
        ).count()
    
    def get_unanswered(self, obj):
        return obj.answers.filter(selected_option__isnull=True).count()
    
    def get_percentage(self, obj):
        total = obj.exam.total_marks
        if total == 0:
            return 0
        return round((obj.score / total) * 100, 2)
