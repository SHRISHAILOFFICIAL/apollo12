from django.db import models
from django.conf import settings
from exams.models import Exam, Question

# Create your models here.


class Attempt(models.Model):
    """Track when a user starts/completes an exam"""
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('timeout', 'Timeout'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts', db_index=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts', db_index=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress', db_index=True)
    randomized_order = models.JSONField(default=list, blank=True, help_text="Array of question IDs in randomized order")
    
    class Meta:
        db_table = 'attempts'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'exam']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.name} {self.exam.year} - {self.status}"


class AttemptAnswer(models.Model):
    """Individual question answers for an exam attempt"""
    
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='answers', db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers', db_index=True)
    selected_option = models.CharField(
        max_length=1, 
        blank=True, 
        null=True,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'attempt_answers'
        unique_together = [['attempt', 'question']]
        indexes = [
            models.Index(fields=['attempt', 'question']),
        ]
    
    def __str__(self):
        return f"Answer for Q{self.question.question_number} in Attempt {self.attempt.id}"


class QuestionIssue(models.Model):
    """Track issues reported by students for questions"""
    
    ISSUE_TYPE_CHOICES = [
        ('wrong_answer', 'Wrong Answer/Incorrect Solution'),
        ('latex_format', 'LaTeX Formatting Issue'),
        ('unclear_question', 'Question is Unclear'),
        ('typo', 'Typo/Spelling Error'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_issues')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reported_issues')
    attempt = models.ForeignKey(Attempt, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_issues')
    
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField(blank=True, help_text="Additional details about the issue")
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', db_index=True)
    admin_notes = models.TextField(blank=True, help_text="Admin notes for resolution")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'question_issues'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['question', 'status']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"Issue: {self.get_issue_type_display()} - Q{self.question.id} by {self.user.username}"

