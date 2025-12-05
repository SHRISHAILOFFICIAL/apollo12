"""
Django management command to create sample DCET exams
Usage: python manage.py create_sample_exams
"""
from django.core.management.base import BaseCommand
from exams.models import Exam, Section, Question


class Command(BaseCommand):
    help = 'Creates sample DCET exams with sections and questions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample DCET exams...'))
        
        # Create DCET 2023 Exam
        exam_2023 = Exam.objects.create(
            name='DCET',
            year=2023,
            total_marks=180,
            duration_minutes=180,  # 3 hours
            is_published=True
        )
        self.stdout.write(f'Created exam: {exam_2023}')
        
        # Create sections for DCET 2023
        sections_data = [
            {'name': 'Mathematics', 'order': 1, 'max_marks': 60},
            {'name': 'Physics', 'order': 2, 'max_marks': 60},
            {'name': 'Chemistry', 'order': 3, 'max_marks': 60},
        ]
        
        for section_data in sections_data:
            section = Section.objects.create(
                exam=exam_2023,
                **section_data
            )
            self.stdout.write(f'  Created section: {section.name}')
            
            # Create sample questions for each section
            self.create_sample_questions(section)
        
        # Create DCET 2024 Exam
        exam_2024 = Exam.objects.create(
            name='DCET',
            year=2024,
            total_marks=180,
            duration_minutes=180,
            is_published=True
        )
        self.stdout.write(f'Created exam: {exam_2024}')
        
        for section_data in sections_data:
            section = Section.objects.create(
                exam=exam_2024,
                **section_data
            )
            self.stdout.write(f'  Created section: {section.name}')
            self.create_sample_questions(section)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample exams created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total exams: {Exam.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total sections: {Section.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total questions: {Question.objects.count()}'))

    def create_sample_questions(self, section):
        """Create sample questions for a section"""
        
        if section.name == 'Mathematics':
            questions_data = [
                {
                    'question_text': 'If f(x) = x² + 2x + 1, what is f(3)?',
                    'option_a': '12',
                    'option_b': '16',
                    'option_c': '18',
                    'option_d': '20',
                    'correct_option': 'B',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the derivative of sin(x)?',
                    'option_a': 'cos(x)',
                    'option_b': '-cos(x)',
                    'option_c': 'tan(x)',
                    'option_d': '-sin(x)',
                    'correct_option': 'A',
                    'marks': 1,
                },
                {
                    'question_text': 'Solve for x: 2x + 5 = 15',
                    'option_a': 'x = 3',
                    'option_b': 'x = 5',
                    'option_c': 'x = 7',
                    'option_d': 'x = 10',
                    'correct_option': 'B',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the value of π (pi) approximately?',
                    'option_a': '3.14',
                    'option_b': '2.71',
                    'option_c': '1.41',
                    'option_d': '1.73',
                    'correct_option': 'A',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the integral of x²?',
                    'option_a': 'x³/3 + C',
                    'option_b': '2x + C',
                    'option_c': 'x³ + C',
                    'option_d': 'x/3 + C',
                    'correct_option': 'A',
                    'marks': 1,
                },
            ]
        elif section.name == 'Physics':
            questions_data = [
                {
                    'question_text': 'What is the SI unit of force?',
                    'option_a': 'Joule',
                    'option_b': 'Newton',
                    'option_c': 'Watt',
                    'option_d': 'Pascal',
                    'correct_option': 'B',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the speed of light in vacuum?',
                    'option_a': '3 × 10⁸ m/s',
                    'option_b': '3 × 10⁶ m/s',
                    'option_c': '3 × 10⁴ m/s',
                    'option_d': '3 × 10² m/s',
                    'correct_option': 'A',
                    'marks': 1,
                },
                {
                    'question_text': 'What is Newton\'s second law of motion?',
                    'option_a': 'F = ma',
                    'option_b': 'E = mc²',
                    'option_c': 'P = VI',
                    'option_d': 'V = IR',
                    'correct_option': 'A',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the acceleration due to gravity on Earth?',
                    'option_a': '9.8 m/s²',
                    'option_b': '10 m/s²',
                    'option_c': '8.9 m/s²',
                    'option_d': '11 m/s²',
                    'correct_option': 'A',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the formula for kinetic energy?',
                    'option_a': 'KE = ½mv²',
                    'option_b': 'KE = mgh',
                    'option_c': 'KE = mv',
                    'option_d': 'KE = ½m²v',
                    'correct_option': 'A',
                    'marks': 1,
                },
            ]
        else:  # Chemistry
            questions_data = [
                {
                    'question_text': 'What is the atomic number of Carbon?',
                    'option_a': '4',
                    'option_b': '6',
                    'option_c': '8',
                    'option_d': '12',
                    'correct_option': 'B',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the chemical formula for water?',
                    'option_a': 'H₂O',
                    'option_b': 'CO₂',
                    'option_c': 'O₂',
                    'option_d': 'H₂SO₄',
                    'correct_option': 'A',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the pH of a neutral solution?',
                    'option_a': '5',
                    'option_b': '7',
                    'option_c': '9',
                    'option_d': '14',
                    'correct_option': 'B',
                    'marks': 1,
                },
                {
                    'question_text': 'What is the symbol for Gold?',
                    'option_a': 'Go',
                    'option_b': 'Gd',
                    'option_c': 'Au',
                    'option_d': 'Ag',
                    'correct_option': 'C',
                    'marks': 1,
                },
                {
                    'question_text': 'What is Avogadro\'s number?',
                    'option_a': '6.022 × 10²³',
                    'option_b': '3.14 × 10⁸',
                    'option_c': '9.8 × 10²',
                    'option_d': '1.6 × 10⁻¹⁹',
                    'correct_option': 'A',
                    'marks': 1,
                },
            ]
        
        for i, q_data in enumerate(questions_data, 1):
            Question.objects.create(
                section=section,
                question_number=i,
                **q_data
            )
