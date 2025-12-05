from rest_framework import serializers
from core.models import Test, Attempt

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'duration', 'total_marks', 'created_at']

class AttemptSerializer(serializers.ModelSerializer):
    test_title = serializers.ReadOnlyField(source='test.title')

    class Meta:
        model = Attempt
        fields = ['id', 'test', 'test_title', 'score', 'completed_at']
