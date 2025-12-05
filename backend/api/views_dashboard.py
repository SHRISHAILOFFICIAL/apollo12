from rest_framework import generics, permissions
from exams.models import Exam
from results.models import Attempt
from exams.serializers import ExamListSerializer
from results.serializers import AttemptSerializer

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.filter(is_published=True)
    serializer_class = ExamListSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserAttemptListView(generics.ListAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attempt.objects.filter(user=self.request.user)
