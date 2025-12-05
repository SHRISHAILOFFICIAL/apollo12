"""
Create sample data for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User
from exams.models import Subject, Exam, Question, Option, ExamSubject
from datetime import datetime, timedelta
from django.utils import timezone

def create_sample_data():
    print("Creating sample data...")
    
    # Create test users
    print("\n1. Creating users...")
    
    # Admin user (if not exists)
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@quiz.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'phone_number': '9876543210',
            'is_staff': True,
            'is_superuser': True,
            'is_student': False,
            'is_teacher': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"   ✓ Created admin user: {admin.username} ({admin.email})")
    else:
        print(f"   - Admin user already exists: {admin.username} ({admin.email})")
    
    # Student user
    student, created = User.objects.get_or_create(
        username='student',
        defaults={
            'email': 'student@quiz.com',
            'first_name': 'Student',
            'last_name': 'Test',
            'phone_number': '9876543211',
            'is_student': True,
            'is_teacher': False
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print(f"   ✓ Created student user: {student.username} ({student.email})")
    else:
        print(f"   - Student user already exists: {student.username} ({student.email})")
    
    # Create subjects
    print("\n2. Creating subjects...")
    subjects_data = [
        {'name': 'Mathematics', 'description': 'Basic and Advanced Mathematics'},
        {'name': 'Physics', 'description': 'Fundamental Physics Concepts'},
        {'name': 'Chemistry', 'description': 'General Chemistry'},
        {'name': 'English', 'description': 'English Language and Literature'},
        {'name': 'Computer Science', 'description': 'Programming and Computer Fundamentals'},
    ]
    
    subjects = []
    for subject_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=subject_data['name'],
            defaults=subject_data
        )
        subjects.append(subject)
        if created:
            print(f"   ✓ Created subject: {subject.name}")
        else:
            print(f"   - Subject already exists: {subject.name}")
    
    # Create exams
    print("\n3. Creating exams...")
    
    # Math Exam
    math_exam, created = Exam.objects.get_or_create(
        title='Mathematics Final Exam',
        defaults={
            'description': 'Comprehensive mathematics examination covering algebra, geometry, and calculus',
            'duration_minutes': 60,
            'total_marks': 15,  # 5 questions
            'is_published': True,
            'created_by': admin
        }
    )
    if created:
        print(f"   ✓ Created exam: {math_exam.title}")
        # Link subjects
        ExamSubject.objects.create(exam=math_exam, subject=subjects[0])
    else:
        print(f"   - Exam already exists: {math_exam.title}")
    
    # Physics Exam
    physics_exam, created = Exam.objects.get_or_create(
        title='Physics Mock Test',
        defaults={
            'description': 'Practice test for physics fundamentals',
            'duration_minutes': 45,
            'total_marks': 7,  # 3 questions
            'is_published': True,
            'created_by': admin
        }
    )
    if created:
        print(f"   ✓ Created exam: {physics_exam.title}")
        ExamSubject.objects.create(exam=physics_exam, subject=subjects[1])
    else:
        print(f"   - Exam already exists: {physics_exam.title}")
    
    # Create questions for Math Exam
    print("\n4. Creating questions for Math Exam...")
    math_questions = [
        {
            'question_text': 'What is the value of π (pi) approximately?',
            'marks': 2,
            'difficulty': 'easy',
            'options': [
                {'text': '2.14', 'correct': False},
                {'text': '3.14', 'correct': True},
                {'text': '4.14', 'correct': False},
                {'text': '5.14', 'correct': False},
            ]
        },
        {
            'question_text': 'What is the square root of 144?',
            'marks': 2,
            'difficulty': 'easy',
            'options': [
                {'text': '10', 'correct': False},
                {'text': '11', 'correct': False},
                {'text': '12', 'correct': True},
                {'text': '13', 'correct': False},
            ]
        },
        {
            'question_text': 'Solve: 2x + 5 = 15. What is x?',
            'marks': 3,
            'difficulty': 'medium',
            'options': [
                {'text': '3', 'correct': False},
                {'text': '4', 'correct': False},
                {'text': '5', 'correct': True},
                {'text': '6', 'correct': False},
            ]
        },
        {
            'question_text': 'What is the derivative of x² with respect to x?',
            'marks': 3,
            'difficulty': 'medium',
            'options': [
                {'text': 'x', 'correct': False},
                {'text': '2x', 'correct': True},
                {'text': 'x²', 'correct': False},
                {'text': '2', 'correct': False},
            ]
        },
        {
            'question_text': 'What is the integral of 2x dx?',
            'marks': 5,
            'difficulty': 'hard',
            'options': [
                {'text': 'x²', 'correct': False},
                {'text': 'x² + C', 'correct': True},
                {'text': '2x²', 'correct': False},
                {'text': '2x² + C', 'correct': False},
            ]
        },
    ]
    
    for q_data in math_questions:
        question, created = Question.objects.get_or_create(
            exam=math_exam,
            question_text=q_data['question_text'],
            defaults={
                'subject': subjects[0],  # Mathematics
                'marks': q_data['marks'],
                'difficulty': q_data['difficulty']
            }
        )
        if created:
            print(f"   ✓ Created question: {question.question_text[:50]}...")
            # Create options
            for opt_data in q_data['options']:
                Option.objects.create(
                    question=question,
                    option_text=opt_data['text'],
                    is_correct=opt_data['correct']
                )
        else:
            print(f"   - Question already exists: {question.question_text[:50]}...")
    
    # Create questions for Physics Exam
    print("\n5. Creating questions for Physics Exam...")
    physics_questions = [
        {
            'question_text': 'What is the SI unit of force?',
            'marks': 2,
            'difficulty': 'easy',
            'options': [
                {'text': 'Joule', 'correct': False},
                {'text': 'Newton', 'correct': True},
                {'text': 'Watt', 'correct': False},
                {'text': 'Pascal', 'correct': False},
            ]
        },
        {
            'question_text': 'What is the speed of light in vacuum?',
            'marks': 2,
            'difficulty': 'easy',
            'options': [
                {'text': '3 × 10⁸ m/s', 'correct': True},
                {'text': '3 × 10⁶ m/s', 'correct': False},
                {'text': '3 × 10⁷ m/s', 'correct': False},
                {'text': '3 × 10⁹ m/s', 'correct': False},
            ]
        },
        {
            'question_text': 'According to Newton\'s second law, F = ?',
            'marks': 3,
            'difficulty': 'medium',
            'options': [
                {'text': 'ma', 'correct': True},
                {'text': 'm/a', 'correct': False},
                {'text': 'a/m', 'correct': False},
                {'text': 'm + a', 'correct': False},
            ]
        },
    ]
    
    for q_data in physics_questions:
        question, created = Question.objects.get_or_create(
            exam=physics_exam,
            question_text=q_data['question_text'],
            defaults={
                'subject': subjects[1],  # Physics
                'marks': q_data['marks'],
                'difficulty': q_data['difficulty']
            }
        )
        if created:
            print(f"   ✓ Created question: {question.question_text[:50]}...")
            for opt_data in q_data['options']:
                Option.objects.create(
                    question=question,
                    option_text=opt_data['text'],
                    is_correct=opt_data['correct']
                )
        else:
            print(f"   - Question already exists: {question.question_text[:50]}...")
    
    print("\n" + "="*60)
    print("Sample data creation completed!")
    print("="*60)
    print("\nTest Credentials:")
    print("  Admin:   admin@quiz.com / admin123")
    print("  Student: student@quiz.com / student123")
    print("\nAvailable Exams:")
    print(f"  - {math_exam.title} ({math_exam.questions.count()} questions)")
    print(f"  - {physics_exam.title} ({physics_exam.questions.count()} questions)")
    print("\nAPI Base URL: http://127.0.0.1:8000/api")
    print("Admin Panel: http://127.0.0.1:8000/admin")
    print("="*60)

if __name__ == '__main__':
    create_sample_data()
