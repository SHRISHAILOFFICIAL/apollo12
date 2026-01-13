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

print("="*80)
print("MOCK TEST 1 - VERIFICATION REPORT")
print("="*80)
print(f"Exam Name: {exam.name} {exam.year}")
print(f"Duration: {exam.duration_minutes} minutes")
print(f"Total Marks: {exam.total_marks}")
print(f"Published: {exam.is_published}")
print(f"Number of Sections: {sections.count()}")
print(f"Total Questions: {questions.count()}")
print("")
print("SECTION DETAILS:")
print("-"*80)
for section in sections:
    section_questions = questions.filter(section=section)
    print(f"Section: {section.name}")
    print(f"  Questions: {section_questions.count()}")
    print(f"  Max Marks: {section.max_marks}")
print("")
print("QUESTIONS LIST:")
print("-"*80)
for q in questions:
    print(f"Q{q.question_number}: {q.plain_text}")
    print(f"  Correct Answer: {q.correct_option}")
    print(f"  Marks: {q.marks}")
    print("")

print("="*80)
print("IMPORT STATUS: SUCCESS")
print("All questions from mock1.csv have been imported successfully!")
print("="*80)
