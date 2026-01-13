#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Exam, Question, Section

# Get Mock Test 1
exam = Exam.objects.get(name='Mock Test', year=1)
questions = Question.objects.filter(section__exam=exam).order_by('question_number')
sections = Section.objects.filter(exam=exam)

print(f"\n{'='*60}")
print(f"Mock Test 1 - Verification Report")
print(f"{'='*60}")
print(f"Exam: {exam.name} {exam.year}")
print(f"Duration: {exam.duration_minutes} minutes")
print(f"Total Marks: {exam.total_marks}")
print(f"Published: {exam.is_published}")
print(f"Sections: {sections.count()}")
print(f"Total Questions: {questions.count()}")
print(f"\nSection Details:")
for section in sections:
    section_questions = questions.filter(section=section)
    print(f"  - {section.name}: {section_questions.count()} questions, {section.max_marks} marks")

print(f"\nQuestions List:")
for q in questions:
    print(f"  Q{q.question_number}: {q.plain_text[:70]}...")

# Publish the exam if not already published
if not exam.is_published:
    exam.is_published = True
    exam.save()
    print(f"\n✅ Exam has been published!")
else:
    print(f"\n✅ Exam is already published!")

print(f"{'='*60}\n")
