from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from exams.models import Question
from results.models import Attempt, QuestionIssue
from .serializers_question_issue import QuestionIssueSerializer

import logging

logger = logging.getLogger(__name__)


class ReportQuestionIssueView(APIView):
    """
    Report an issue with a question during an exam.
    
    POST /api/exam/report-issue/
    
    Request Body:
    {
        "question_id": 123,
        "attempt_id": 456,
        "issue_type": "wrong_answer",
        "description": "Optional description"
    }
    
    Response:
    {
        "id": 789,
        "message": "Issue reported successfully"
    }
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Submit a question issue report."""
        
        # Validate request data
        serializer = QuestionIssueSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question_id = serializer.validated_data['question_id']
        attempt_id = serializer.validated_data.get('attempt_id')
        issue_type = serializer.validated_data['issue_type']
        description = serializer.validated_data.get('description', '')
        
        # Validate question exists
        question = get_object_or_404(Question, id=question_id)
        
        # Validate attempt if provided
        attempt = None
        if attempt_id:
            attempt = get_object_or_404(Attempt, id=attempt_id)
            if attempt.user != request.user:
                return Response(
                    {"error": "This attempt does not belong to you."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        try:
            # Create issue report
            issue = QuestionIssue.objects.create(
                user=request.user,
                question=question,
                attempt=attempt,
                issue_type=issue_type,
                description=description
            )
            
            logger.info(f"Issue reported by {request.user.username} for question {question_id}: {issue_type}")
            
            return Response(
                {
                    "id": issue.id,
                    "message": "Issue reported successfully. Thank you for your feedback!"
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Error creating issue report: {str(e)}")
            return Response(
                {"error": "Failed to submit issue report. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
