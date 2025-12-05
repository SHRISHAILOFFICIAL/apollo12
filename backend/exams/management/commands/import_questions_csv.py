"""
Django management command to import questions from CSV file
Usage: python manage.py import_questions_csv <exam_name> <year> <csv_file_path>
Example: python manage.py import_questions_csv "PYQ" 2023 questions.csv

CSV Format:
section_name,question_number,question_text,option_a,option_b,option_c,option_d,correct_option,marks
Mathematics,1,What is 2+2?,3,4,5,6,B,1
"""
import csv
from django.core.management.base import BaseCommand, CommandError
from exams.models import Exam, Section, Question


class Command(BaseCommand):
    help = 'Import questions from CSV file into an exam'

    def add_arguments(self, parser):
        parser.add_argument('exam_name', type=str, help='Name of the exam (e.g., PYQ)')
        parser.add_argument('year', type=int, help='Year of the exam (e.g., 2023)')
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
        parser.add_argument(
            '--duration',
            type=int,
            default=180,
            help='Exam duration in minutes (default: 180)'
        )

    def handle(self, *args, **options):
        exam_name = options['exam_name']
        year = options['year']
        csv_file = options['csv_file']
        duration = options['duration']

        self.stdout.write(self.style.SUCCESS(f'\n📚 Importing questions for {exam_name} {year}...'))

        # Create or get exam
        exam, created = Exam.objects.get_or_create(
            name=exam_name,
            year=year,
            defaults={
                'duration_minutes': duration,
                'is_published': False,  # Set to False initially
                'total_marks': 0  # Will calculate later
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created new exam: {exam}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Using existing exam: {exam}'))

        # Read CSV and import questions
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Validate CSV headers
                required_fields = ['section_name', 'question_number', 'question_text', 
                                 'option_a', 'option_b', 'option_c', 'option_d', 
                                 'correct_option']
                
                if not all(field in reader.fieldnames for field in required_fields):
                    raise CommandError(f'CSV must have these columns: {", ".join(required_fields)}')

                sections_created = {}
                questions_imported = 0
                total_marks = 0

                for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                    try:
                        section_name = row['section_name'].strip()
                        question_number = int(row['question_number'])
                        marks = int(row.get('marks', 1))

                        # Create or get section
                        if section_name not in sections_created:
                            # Determine section order
                            section_order = len(sections_created) + 1
                            section, sec_created = Section.objects.get_or_create(
                                exam=exam,
                                name=section_name,
                                defaults={
                                    'order': section_order,
                                    'max_marks': 0  # Will calculate
                                }
                            )
                            sections_created[section_name] = section
                            if sec_created:
                                self.stdout.write(f'  📁 Created section: {section_name}')
                        else:
                            section = sections_created[section_name]

                        # Create question
                        question, q_created = Question.objects.update_or_create(
                            section=section,
                            question_number=question_number,
                            defaults={
                                'question_text': row['question_text'].strip(),
                                'plain_text': row.get('plain_text', '').strip(),
                                'option_a': row['option_a'].strip(),
                                'option_b': row['option_b'].strip(),
                                'option_c': row['option_c'].strip(),
                                'option_d': row['option_d'].strip(),
                                'correct_option': row['correct_option'].strip().upper(),
                                'marks': marks,
                                'diagram_url': row.get('diagram_url', '').strip() or None
                            }
                        )

                        if q_created:
                            questions_imported += 1
                            total_marks += marks
                        else:
                            self.stdout.write(self.style.WARNING(
                                f'  ⚠️  Updated existing question: {section_name} Q{question_number}'
                            ))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'  ❌ Error at row {row_num}: {str(e)}'
                        ))
                        continue

                # Update exam total marks
                exam.total_marks = total_marks
                exam.save()

                # Update section max_marks
                for section in sections_created.values():
                    section_marks = sum(q.marks for q in section.questions.all())
                    section.max_marks = section_marks
                    section.save()

                self.stdout.write(self.style.SUCCESS(f'\n✅ Import completed!'))
                self.stdout.write(self.style.SUCCESS(f'   Exam: {exam}'))
                self.stdout.write(self.style.SUCCESS(f'   Sections: {len(sections_created)}'))
                self.stdout.write(self.style.SUCCESS(f'   Questions imported: {questions_imported}'))
                self.stdout.write(self.style.SUCCESS(f'   Total marks: {total_marks}'))
                self.stdout.write(self.style.SUCCESS(f'\n💡 To publish this exam, run:'))
                self.stdout.write(self.style.SUCCESS(f'   python manage.py shell'))
                self.stdout.write(self.style.SUCCESS(f'   >>> from exams.models import Exam'))
                self.stdout.write(self.style.SUCCESS(f'   >>> exam = Exam.objects.get(name="{exam_name}", year={year})'))
                self.stdout.write(self.style.SUCCESS(f'   >>> exam.is_published = True'))
                self.stdout.write(self.style.SUCCESS(f'   >>> exam.save()'))

        except FileNotFoundError:
            raise CommandError(f'CSV file not found: {csv_file}')
        except Exception as e:
            raise CommandError(f'Error reading CSV: {str(e)}')
