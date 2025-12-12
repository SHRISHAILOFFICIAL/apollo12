from django.db import models
from django.conf import settings

# Create your models here.


class Exam(models.Model):
    """Exam/Mock Test metadata"""
    
    name = models.CharField(max_length=100)  # e.g., "DCET"
    year = models.IntegerField()  # e.g., 2023
    total_marks = models.IntegerField(default=0)
    duration_minutes = models.IntegerField()
    
    # Video solution
    solution_video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube URL for complete paper solution video"
    )
    
    # Access control
    ACCESS_TIER_CHOICES = [
        ('FREE', 'Free Access'),
        ('PRO', 'Pro Access'),
    ]
    access_tier = models.CharField(
        max_length=10,
        choices=ACCESS_TIER_CHOICES,
        default='PRO',
        db_index=True,
        help_text="Minimum tier required to access this exam"
    )
    
    is_published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exams'
        ordering = ['-year', 'name']
        indexes = [
            models.Index(fields=['is_published']),
            models.Index(fields=['year']),
            models.Index(fields=['access_tier']),
        ]
    
    @property
    def is_premium(self):
        """Check if exam requires PRO tier"""
        return self.access_tier == 'PRO'
    
    @property
    def title(self):
        """Return formatted title for frontend compatibility"""
        return f"{self.name} {self.year}"
    
    @property
    def description(self):
        """Return description for frontend"""
        return f"Mock test for {self.name} examination - {self.year}"
    
    def __str__(self):
        return f"{self.name} {self.year}"


class Section(models.Model):
    """Sections within an exam (e.g., Engineering Mathematics, Statistics, etc.)"""
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections', db_index=True)
    name = models.CharField(max_length=200)  # e.g., "ENGINEERING MATHEMATICS"
    order = models.IntegerField()  # Display order
    max_marks = models.IntegerField(default=20)
    
    class Meta:
        db_table = 'sections'
        ordering = ['exam', 'order']
        unique_together = [['exam', 'order']]
        indexes = [
            models.Index(fields=['exam', 'order']),
        ]
    
    def __str__(self):
        return f"{self.exam.name} - {self.name}"


class Question(models.Model):
    """Questions belonging to a section"""
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions', db_index=True)
    question_number = models.IntegerField()  # 1-20 within section
    question_text = models.TextField(help_text="Supports LaTeX formatting")
    plain_text = models.TextField(blank=True, help_text="Plain text version without LaTeX")
    
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    
    correct_option = models.CharField(
        max_length=1, 
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    
    marks = models.IntegerField(default=1)
    diagram_url = models.URLField(blank=True, null=True, help_text="Optional diagram/image URL")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['section', 'question_number']
        unique_together = [['section', 'question_number']]
        indexes = [
            models.Index(fields=['section', 'question_number']),
        ]
    
    def __str__(self):
        return f"{self.section.name} Q{self.question_number}"
