from rest_framework import generics, permissions
from core.models import Test, Attempt
from .serializers_test import TestSerializer, AttemptSerializer

class TestListView(generics.ListAPIView):
    queryset = Test.objects.filter(is_published=True)
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserAttemptListView(generics.ListAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attempt.objects.filter(user=self.request.user)
