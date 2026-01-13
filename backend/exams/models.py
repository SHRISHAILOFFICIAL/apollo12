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
    
    # Availability window for scheduling
    available_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Exam becomes available from this time"
    )
    available_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Exam available until this time"
    )
    
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
    def is_available(self):
        """Check if exam is currently available based on time window"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_published:
            return False
        
        if self.available_from and now < self.available_from:
            return False
        
        if self.available_until and now > self.available_until:
            return False
        
        return True
    
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


class Note(models.Model):
    """Study notes for different subjects"""
    
    ACCESS_TIERS = [
        ('FREE', 'Free'),
        ('PRO', 'PRO Only'),
    ]
    
    subject = models.CharField(max_length=200, help_text="Subject name (e.g., Engineering Mathematics)")
    topic = models.CharField(max_length=200, help_text="Topic name (e.g., Matrices)")
    description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, help_text="Relative path from notes directory (e.g., engineering_mathematics/matrix_notes.pdf)")
    access_tier = models.CharField(max_length=10, choices=ACCESS_TIERS, default='FREE', db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.IntegerField(default=0, help_text="Display order within subject")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notes'
        ordering = ['subject', 'order', 'topic']
        indexes = [
            models.Index(fields=['subject', 'is_active']),
            models.Index(fields=['access_tier']),
        ]
        
    @property
    def is_premium(self):
        """Check if note requires PRO tier"""
        return self.access_tier == 'PRO'
        
    def __str__(self):
        return f"{self.subject} - {self.topic}"


class PYQ(models.Model):
    """Previous Year Question Papers"""
    
    ACCESS_TIERS = [
        ('FREE', 'Free'),
        ('PRO', 'PRO Only'),
    ]
    
    exam_name = models.CharField(max_length=200, help_text="Exam name (e.g., DCET, Mock Test 1)")
    year = models.IntegerField(help_text="Year of the exam (e.g., 2023, 2024)")
    description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, help_text="Relative path from pyqs directory")
    access_tier = models.CharField(max_length=10, choices=ACCESS_TIERS, default='FREE', db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.IntegerField(default=0, help_text="Display order within year")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pyqs'
        ordering = ['-year', 'order', 'exam_name']
        indexes = [
            models.Index(fields=['year', 'is_active']),
            models.Index(fields=['access_tier']),
        ]
        
    @property
    def is_premium(self):
        """Check if PYQ requires PRO tier"""
        return self.access_tier == 'PRO'
        
    def __str__(self):
        return f"{self.exam_name} {self.year}"


class VideoSolution(models.Model):
    """Video Solutions (PRO only)"""
    
    topic = models.CharField(max_length=200, help_text="Topic name (e.g., Matrices, Calculus)")
    title = models.CharField(max_length=300, help_text="Video title")
    description = models.TextField(blank=True)
    youtube_url = models.URLField(help_text="YouTube video URL")
    duration_minutes = models.IntegerField(default=0, help_text="Video duration in minutes")
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.IntegerField(default=0, help_text="Display order within topic")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'video_solutions'
        ordering = ['topic', 'order', 'title']
        indexes = [
            models.Index(fields=['topic', 'is_active']),
        ]
        
    def __str__(self):
        return f"{self.topic} - {self.title}"


class Announcement(models.Model):
    """Announcements for exam dates, results, and general updates"""
    
    TYPE_CHOICES = [
        ('GENERAL', 'General'),
        ('EXAM_DATE', 'Exam Date'),
        ('RESULTS', 'Results'),
        ('URGENT', 'Urgent'),
    ]
    
    title = models.CharField(max_length=300)
    message = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='GENERAL')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]
        
    def __str__(self):
        return f"[{self.announcement_type}] {self.title}"
