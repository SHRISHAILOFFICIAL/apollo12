from rest_framework import generics, permissions, status
from rest_framework.response import Response as APIResponse
from rest_framework.views import APIView
from django.utils import timezone
from core.models import Test, Attempt, Question, Response
from .serializers_test import TestSerializer, AttemptSerializer

class StartTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
            # Check if ongoing attempt exists
            attempt, created = Attempt.objects.get_or_create(
                user=request.user,
                test=test,
                status='ongoing'
            )
            if created:
                attempt.save()
            
            # Return test data and attempt id
            questions = test.questions.all()
            questions_data = [{
                'id': q.id,
                'text': q.text,
                'options': {
                    'A': q.option_a,
                    'B': q.option_b,
                    'C': q.option_c,
                    'D': q.option_d
                },
                'marks': q.marks
            } for q in questions]

            return APIResponse({
                'attempt_id': attempt.id,
                'duration': test.duration,
                'questions': questions_data
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return APIResponse({'error': str(e)}, status=500)

class SubmitAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        attempt_id = request.data.get('attempt_id')
        question_id = request.data.get('question_id')
        selected_option = request.data.get('selected_option')
        
        attempt = Attempt.objects.get(id=attempt_id, user=request.user)
        if attempt.status == 'completed':
            return APIResponse({'error': 'Test already completed'}, status=400)

        question = Question.objects.get(id=question_id)
        
        response, created = Response.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={'selected_option': selected_option}
        )
        
        return APIResponse({'status': 'saved'})

class SubmitTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        attempt_id = request.data.get('attempt_id')
        attempt = Attempt.objects.get(id=attempt_id, user=request.user)
        
        if attempt.status == 'completed':
            return APIResponse({'message': 'Already submitted'})

        # Calculate Score
        score = 0
        responses = attempt.responses.all()
        for resp in responses:
            if resp.selected_option == resp.question.correct_option:
                score += resp.question.marks
        
        attempt.score = score
        attempt.status = 'completed'
        attempt.completed_at = timezone.now()
        attempt.save()
        
        return APIResponse({'score': score, 'total_marks': attempt.test.total_marks})
