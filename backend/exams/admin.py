from django.contrib import admin
from .models import Exam, Section, Question

# Register your models here.


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ['name', 'order', 'max_marks']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ['question_number', 'question_text', 'correct_option', 'marks']
    show_change_link = True


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'total_marks', 'duration_minutes', 'is_published', 'created_at']
    list_filter = ['is_published', 'year', 'created_at']
    search_fields = ['name']
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'name', 'order', 'max_marks', 'question_count']
    list_filter = ['exam']
    search_fields = ['name', 'exam__name']
    raw_id_fields = ['exam']
    inlines = [QuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['section', 'question_number', 'short_text', 'correct_option', 'marks']
    list_filter = ['section__exam', 'section', 'correct_option']
    search_fields = ['question_text', 'plain_text']
    raw_id_fields = ['section']
    
    fieldsets = [
        ('Question Info', {
            'fields': ['section', 'question_number', 'marks']
        }),
        ('Question Content', {
            'fields': ['question_text', 'plain_text', 'diagram_url']
        }),
        ('Options', {
            'fields': ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        }),
    ]
    
    def short_text(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    short_text.short_description = 'Question'
