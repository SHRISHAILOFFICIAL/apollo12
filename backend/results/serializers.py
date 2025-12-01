from rest_framework import serializers
from .models import ExamAttempt, AttemptResponse
from exams.models import Question, Option, Exam
from users.models import User


class AttemptResponseSerializer(serializers.ModelSerializer):
    """Serializer for individual question responses"""
    
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    selected_option_text = serializers.CharField(source='selected_option.option_text', read_only=True)
    correct_answer = serializers.SerializerMethodField()
    
    class Meta:
        model = AttemptResponse
        fields = [
            'id', 'attempt', 'question', 'question_text',
            'selected_option', 'selected_option_text',
            'is_correct', 'correct_answer'
        ]
        read_only_fields = ['id', 'is_correct']
    
    def get_correct_answer(self, obj):
        """Return correct option only after attempt is submitted"""
        if obj.attempt.status in ['submitted', 'timeout']:
            correct_option = obj.question.options.filter(is_correct=True).first()
            if correct_option:
                return {
                    'id': correct_option.id,
                    'option_text': correct_option.option_text
                }
        return None


class AttemptResponseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating responses during exam"""
    
    class Meta:
        model = AttemptResponse
        fields = ['id', 'attempt', 'question', 'selected_option']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Create response and check if answer is correct"""
        response = AttemptResponse(**validated_data)
        
        # Check if selected option is correct
        if response.selected_option:
            response.is_correct = response.selected_option.is_correct
        
        response.save()
        return response
    
    def update(self, instance, validated_data):
        """Update response and recheck correctness"""
        instance.selected_option = validated_data.get('selected_option', instance.selected_option)
        
        # Recheck correctness
        if instance.selected_option:
            instance.is_correct = instance.selected_option.is_correct
        else:
            instance.is_correct = None
        
        instance.save()
        return instance


class ExamAttemptSerializer(serializers.ModelSerializer):
    """Serializer for exam attempts"""
    
    user_name = serializers.CharField(source='user.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    responses_count = serializers.SerializerMethodField()
    duration_minutes = serializers.IntegerField(source='exam.duration_minutes', read_only=True)
    
    class Meta:
        model = ExamAttempt
        fields = [
            'id', 'user', 'user_name', 'exam', 'exam_title',
            'start_time', 'end_time', 'score', 'status',
            'responses_count', 'duration_minutes'
        ]
        read_only_fields = ['id', 'start_time', 'score']
    
    def get_responses_count(self, obj):
        return obj.responses.count()


class ExamAttemptDetailSerializer(serializers.ModelSerializer):
    """Detailed exam attempt with all responses"""
    
    responses = AttemptResponseSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    total_questions = serializers.SerializerMethodField()
    answered_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamAttempt
        fields = [
            'id', 'user', 'user_name', 'exam', 'exam_title',
            'start_time', 'end_time', 'score', 'status',
            'total_questions', 'answered_questions', 'correct_answers',
            'responses'
        ]
        read_only_fields = ['id', 'start_time']
    
    def get_total_questions(self, obj):
        return obj.exam.questions.count()
    
    def get_answered_questions(self, obj):
        return obj.responses.filter(selected_option__isnull=False).count()
    
    def get_correct_answers(self, obj):
        return obj.responses.filter(is_correct=True).count()


class ExamAttemptStartSerializer(serializers.Serializer):
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


class ExamAttemptSubmitSerializer(serializers.Serializer):
    """Serializer for submitting an exam"""
    
    attempt_id = serializers.IntegerField()
    
    def validate_attempt_id(self, value):
        """Validate attempt exists and belongs to user"""
        user = self.context.get('user')
        try:
            attempt = ExamAttempt.objects.get(id=value, user=user)
            if attempt.status != 'in_progress':
                raise serializers.ValidationError("This attempt is already completed")
            return value
        except ExamAttempt.DoesNotExist:
            raise serializers.ValidationError("Attempt not found")


class ExamResultSerializer(serializers.ModelSerializer):
    """Serializer for exam results/summary"""
    
    user_name = serializers.CharField(source='user.name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    total_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    wrong_answers = serializers.SerializerMethodField()
    unanswered = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamAttempt
        fields = [
            'id', 'user_name', 'exam_title', 'start_time', 'end_time',
            'score', 'total_questions', 'correct_answers', 'wrong_answers',
            'unanswered', 'percentage', 'status'
        ]
    
    def get_total_questions(self, obj):
        return obj.exam.questions.count()
    
    def get_correct_answers(self, obj):
        return obj.responses.filter(is_correct=True).count()
    
    def get_wrong_answers(self, obj):
        return obj.responses.filter(is_correct=False).count()
    
    def get_unanswered(self, obj):
        return obj.responses.filter(selected_option__isnull=True).count()
    
    def get_percentage(self, obj):
        total = self.get_total_questions(obj)
        if total == 0:
            return 0
        return round((obj.score / obj.exam.total_marks) * 100, 2)
