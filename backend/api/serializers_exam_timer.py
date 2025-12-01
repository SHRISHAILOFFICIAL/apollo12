"""
Serializers for exam timer operations.

These serializers handle data validation and formatting for:
- Starting exams with Redis timers
- Checking remaining time
- Submitting exams
"""

from rest_framework import serializers
from core.models import Test, Attempt, Question


class StartExamSerializer(serializers.Serializer):
    """
    Serializer for starting an exam.
    
    Validates that exam exists and is published.
    """
    exam_id = serializers.IntegerField(required=True)
    
    def validate_exam_id(self, value):
        """Validate that exam exists and is published."""
        try:
            exam = Test.objects.get(id=value)
            if not exam.is_published:
                raise serializers.ValidationError("This exam is not published yet.")
            return value
        except Test.DoesNotExist:
            raise serializers.ValidationError("Exam not found.")


class StartExamResponseSerializer(serializers.Serializer):
    """
    Response serializer for starting an exam.
    
    Returns attempt ID, exam ID, and initial remaining time.
    """
    attempt_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    exam_title = serializers.CharField()
    duration_minutes = serializers.IntegerField()
    remaining_seconds = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    total_marks = serializers.IntegerField()


class RemainingTimeResponseSerializer(serializers.Serializer):
    """
    Response serializer for checking remaining time.
    
    Returns current status and remaining seconds.
    """
    status = serializers.ChoiceField(choices=['running', 'timeout', 'completed'])
    remaining_seconds = serializers.IntegerField()
    message = serializers.CharField(required=False)


class SubmitAnswerSerializer(serializers.Serializer):
    """
    Serializer for submitting an answer to a question.
    
    Validates attempt, question, and selected option.
    """
    attempt_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    selected_option = serializers.ChoiceField(
        choices=['A', 'B', 'C', 'D'],
        required=True
    )
    
    def validate_attempt_id(self, value):
        """Validate that attempt exists."""
        try:
            Attempt.objects.get(id=value)
            return value
        except Attempt.DoesNotExist:
            raise serializers.ValidationError("Exam attempt not found.")
    
    def validate_question_id(self, value):
        """Validate that question exists."""
        try:
            Question.objects.get(id=value)
            return value
        except Question.DoesNotExist:
            raise serializers.ValidationError("Question not found.")


class SubmitExamSerializer(serializers.Serializer):
    """
    Serializer for submitting an exam.
    
    Validates that attempt exists and belongs to the user.
    """
    attempt_id = serializers.IntegerField(required=True)
    
    def validate_attempt_id(self, value):
        """Validate that attempt exists."""
        try:
            Attempt.objects.get(id=value)
            return value
        except Attempt.DoesNotExist:
            raise serializers.ValidationError("Exam attempt not found.")


class SubmitExamResponseSerializer(serializers.Serializer):
    """
    Response serializer for exam submission.
    
    Returns final score and exam completion details.
    """
    status = serializers.ChoiceField(choices=['submitted', 'timeout', 'already_completed'])
    score = serializers.IntegerField()
    total_marks = serializers.IntegerField()
    percentage = serializers.FloatField()
    correct_answers = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    time_taken_minutes = serializers.IntegerField(required=False)
    message = serializers.CharField(required=False)


class QuestionResponseSerializer(serializers.Serializer):
    """
    Serializer for question data returned when starting exam.
    
    Does not expose correct answers.
    """
    id = serializers.IntegerField()
    text = serializers.CharField()
    option_a = serializers.CharField()
    option_b = serializers.CharField()
    option_c = serializers.CharField()
    option_d = serializers.CharField()
    marks = serializers.IntegerField()
