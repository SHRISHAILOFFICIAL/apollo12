from rest_framework import serializers
from results.models import QuestionIssue


class QuestionIssueSerializer(serializers.Serializer):
    """Serializer for question issue reports"""
    
    question_id = serializers.IntegerField(required=True)
    attempt_id = serializers.IntegerField(required=False, allow_null=True)
    issue_type = serializers.ChoiceField(
        choices=QuestionIssue.ISSUE_TYPE_CHOICES,
        required=True
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000
    )
