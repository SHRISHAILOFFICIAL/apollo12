"""
Django admin configuration for results models
"""
from django.contrib import admin
from .models import Attempt, AttemptAnswer, QuestionIssue


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'status', 'started_at', 'finished_at']
    list_filter = ['status', 'exam', 'started_at']
    search_fields = ['user__username', 'exam__name']
    readonly_fields = ['started_at']
    
    fieldsets = (
        ('Attempt Info', {
            'fields': ('user', 'exam', 'status')
        }),
        ('Timing', {
            'fields': ('started_at', 'finished_at')
        }),
        ('Results', {
            'fields': ('score', 'randomized_order')
        }),
    )


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_option', 'is_correct']
    list_filter = ['attempt__exam', 'selected_option']
    search_fields = ['attempt__user__username', 'question__question_text']


@admin.register(QuestionIssue)
class QuestionIssueAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'issue_type', 'status', 'created_at']
    list_filter = ['issue_type', 'status', 'created_at']
    search_fields = ['user__username', 'question__question_text', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Issue Info', {
            'fields': ('user', 'question', 'attempt')
        }),
        ('Issue Details', {
            'fields': ('issue_type', 'description')
        }),
        ('Resolution', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
