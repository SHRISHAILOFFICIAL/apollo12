"""
Django admin configuration for exam models
"""
from django.contrib import admin
from .models import Exam, Section, Question


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'access_tier', 'total_marks', 'duration_minutes', 'is_published', 'created_at']
    list_filter = ['access_tier', 'is_published', 'year']
    search_fields = ['name', 'year']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'year', 'total_marks', 'duration_minutes')
        }),
        ('Access Control', {
            'fields': ('access_tier', 'is_published')
        }),
        ('Solution Video', {
            'fields': ('solution_video_url',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'name', 'order', 'max_marks']
    list_filter = ['exam']
    search_fields = ['name', 'exam__name']
    ordering = ['exam', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['section', 'question_number', 'correct_option', 'marks']
    list_filter = ['section__exam', 'correct_option']
    search_fields = ['question_text', 'section__name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Question Info', {
            'fields': ('section', 'question_number', 'marks')
        }),
        ('Question Text', {
            'fields': ('question_text', 'plain_text', 'diagram_url')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_option')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
