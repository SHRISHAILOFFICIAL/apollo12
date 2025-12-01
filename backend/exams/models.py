from django.db import models
from django.conf import settings

# Create your models here.


class Subject(models.Model):
    """Subject categories for questions"""
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subjects'
    
    def __str__(self):
        return self.name


class Exam(models.Model):
    """Exam/Mock Test metadata"""
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField()
    total_marks = models.IntegerField(default=0)
    
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_exams')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exams'
        indexes = [
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return self.title


class ExamSubject(models.Model):
    """Many-to-many relationship between exams and subjects"""
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_subjects', db_index=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_subjects', db_index=True)
    
    class Meta:
        db_table = 'exam_subjects'
        unique_together = ['exam', 'subject']
    
    def __str__(self):
        return f"{self.exam.title} - {self.subject.name}"


class Question(models.Model):
    """Questions belonging to an exam"""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', db_index=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', db_index=True)
    
    question_text = models.TextField()
    marks = models.IntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'questions'
        indexes = [
            models.Index(fields=['exam']),
            models.Index(fields=['subject']),
        ]
    
    def __str__(self):
        return f"Q{self.id} - {self.exam.title}"


class Option(models.Model):
    """MCQ options for questions"""
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', db_index=True)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'options'
    
    def __str__(self):
        return f"Option for Q{self.question.id}"
