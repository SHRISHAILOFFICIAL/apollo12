from django.contrib import admin
from .models import Attempt, AttemptAnswer

# Register your models here.


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    extra = 0
    fields = ['question', 'selected_option', 'is_correct']
    raw_id_fields = ['question']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'status', 'started_at', 'finished_at']
    list_filter = ['status', 'exam', 'started_at']
    search_fields = ['user__username', 'exam__name']
    raw_id_fields = ['user', 'exam']
    readonly_fields = ['started_at']
    inlines = [AttemptAnswerInline]


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_option', 'is_correct']
    list_filter = ['is_correct', 'selected_option']
    search_fields = ['attempt__user__username', 'question__question_text']
    raw_id_fields = ['attempt', 'question']
