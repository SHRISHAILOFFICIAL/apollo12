from rest_framework import generics, permissions, status
from rest_framework.response import Response as APIResponse
from rest_framework.views import APIView
from django.utils import timezone
from exams.models import Exam, Question
from results.models import Attempt, AttemptAnswer
from exams.serializers import ExamSerializer
from results.serializers import AttemptSerializer

class StartExamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
            # Check if ongoing attempt exists
            attempt, created = Attempt.objects.get_or_create(
                user=request.user,
                exam=exam,
                status='in_progress'
            )
            if created:
                # Create empty answers for all questions
                questions = Question.objects.filter(section__exam=exam)
                for question in questions:
                    AttemptAnswer.objects.create(
                        attempt=attempt,
                        question=question
                    )
            
            # Return exam data and attempt id
            questions = Question.objects.filter(section__exam=exam).order_by('section__order', 'question_number')
            questions_data = [{
                'id': q.id,
                'section': q.section.name,
                'question_number': q.question_number,
                'text': q.question_text,
                'plain_text': q.plain_text,
                'options': {
                    'A': q.option_a,
                    'B': q.option_b,
                    'C': q.option_c,
                    'D': q.option_d
                },
                'marks': q.marks,
                'diagram_url': q.diagram_url
            } for q in questions]

            return APIResponse({
                'attempt_id': attempt.id,
                'duration': exam.duration_minutes,
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
        selected_option = request.data.get('selected_option')  # A/B/C/D
        
        attempt = Attempt.objects.get(id=attempt_id, user=request.user)
        if attempt.status == 'submitted':
            return APIResponse({'error': 'Exam already submitted'}, status=400)

        question = Question.objects.get(id=question_id)
        
        answer, created = AttemptAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={
                'selected_option': selected_option,
                'is_correct': (selected_option == question.correct_option) if selected_option else False
            }
        )
        
        return APIResponse({'status': 'saved'})

class SubmitExamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        attempt_id = request.data.get('attempt_id')
        attempt = Attempt.objects.get(id=attempt_id, user=request.user)
        
        if attempt.status == 'submitted':
            return APIResponse({'message': 'Already submitted'})

        # Calculate Score
        score = 0
        answers = attempt.answers.all()
        for answer in answers:
            if answer.is_correct:
                score += answer.question.marks
        
        attempt.score = score
        attempt.status = 'submitted'
        attempt.finished_at = timezone.now()
        attempt.save()
        
        return APIResponse({'score': score, 'total_marks': attempt.exam.total_marks})
