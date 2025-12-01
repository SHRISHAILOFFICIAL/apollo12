from django.db import models
from django.conf import settings
from exams.models import Exam, Question, Option

# Create your models here.


class ExamAttempt(models.Model):
    """Track when a user starts/completes an exam"""
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('timeout', 'Timeout'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_attempts', db_index=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts', db_index=True)
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    
    class Meta:
        db_table = 'exam_attempts'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['exam']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.status}"


class AttemptResponse(models.Model):
    """Individual question answers for an exam attempt"""
    
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='responses', db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses', db_index=True)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, blank=True, null=True, related_name='student_selections')
    is_correct = models.BooleanField(blank=True, null=True)
    
    class Meta:
        db_table = 'attempt_responses'
    
    def __str__(self):
        return f"Response for Q{self.question.id} in Attempt {self.attempt.id}"
