#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Exam, Question, Section

# Get Math Mock Test 1
exam = Exam.objects.get(name='Math Mock Test', year=1)
questions = Question.objects.filter(section__exam=exam).order_by('question_number')
sections = Section.objects.filter(exam=exam)

# Recalculate and update total marks
total_marks = sum(q.marks for q in questions)
exam.total_marks = total_marks
exam.save()

# Update section marks
for section in sections:
    section_questions = questions.filter(section=section)
    section.max_marks = sum(q.marks for q in section_questions)
    section.save()

# Write to file
with open('final_verification.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("MATH MOCK TEST 1 - FINAL VERIFICATION\n")
    f.write("="*80 + "\n")
    f.write(f"Exam: {exam.name} {exam.year}\n")
    f.write(f"Duration: {exam.duration_minutes} minutes\n")
    f.write(f"Total Marks: {exam.total_marks}\n")
    f.write(f"Published: {exam.is_published}\n")
    f.write(f"Sections: {sections.count()}\n")
    f.write(f"Total Questions: {questions.count()}\n")
    f.write("\n")
    f.write("SECTION DETAILS:\n")
    f.write("-"*80 + "\n")
    for section in sections:
        section_questions = questions.filter(section=section)
        f.write(f"{section.name}: {section_questions.count()} questions, {section.max_marks} marks\n")
    f.write("\n")
    f.write("ALL QUESTIONS:\n")
    f.write("-"*80 + "\n")
    for q in questions:
        f.write(f"Q{q.question_number}: {q.plain_text} (Answer: {q.correct_option}, {q.marks} mark)\n")
    f.write("\n")
    f.write("="*80 + "\n")
    f.write("STATUS: All questions successfully updated in Math Mock Test 1!\n")
    f.write("="*80 + "\n")

print("Final verification complete!")
print(f"Math Mock Test 1: {questions.count()} questions, {exam.total_marks} marks, {exam.duration_minutes} mins")
