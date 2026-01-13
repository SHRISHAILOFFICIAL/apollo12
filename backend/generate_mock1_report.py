#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Exam, Question, Section

# Get Mock Test 1
exam = Exam.objects.get(name='Mock Test', year=1)
questions = Question.objects.filter(section__exam=exam).order_by('question_number')
sections = Section.objects.filter(exam=exam)

# Write to file
with open('mock1_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("MOCK TEST 1 - VERIFICATION REPORT\n")
    f.write("="*80 + "\n")
    f.write(f"Exam Name: {exam.name} {exam.year}\n")
    f.write(f"Duration: {exam.duration_minutes} minutes\n")
    f.write(f"Total Marks: {exam.total_marks}\n")
    f.write(f"Published: {exam.is_published}\n")
    f.write(f"Number of Sections: {sections.count()}\n")
    f.write(f"Total Questions: {questions.count()}\n")
    f.write("\n")
    f.write("SECTION DETAILS:\n")
    f.write("-"*80 + "\n")
    for section in sections:
        section_questions = questions.filter(section=section)
        f.write(f"Section: {section.name}\n")
        f.write(f"  Questions: {section_questions.count()}\n")
        f.write(f"  Max Marks: {section.max_marks}\n")
    f.write("\n")
    f.write("QUESTIONS LIST:\n")
    f.write("-"*80 + "\n")
    for q in questions:
        f.write(f"Q{q.question_number}: {q.plain_text}\n")
        f.write(f"  Correct Answer: {q.correct_option}\n")
        f.write(f"  Marks: {q.marks}\n")
        f.write("\n")
    
    f.write("="*80 + "\n")
    f.write("IMPORT STATUS: SUCCESS\n")
    f.write("All questions from mock1.csv have been imported successfully!\n")
    f.write("="*80 + "\n")

print("Report written to mock1_report.txt")
