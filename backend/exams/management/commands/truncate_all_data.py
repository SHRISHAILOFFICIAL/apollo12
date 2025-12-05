from django.core.management.base import BaseCommand
from django.db import transaction
from exams.models import Exam, Section, Question
from results.models import Attempt, AttemptAnswer


class Command(BaseCommand):
    help = 'Truncate all data from exams, sections, questions, attempts, and attempt_answers tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        # Show current counts
        self.stdout.write(self.style.WARNING('\n=== Current Database State ==='))
        exam_count = Exam.objects.count()
        section_count = Section.objects.count()
        question_count = Question.objects.count()
        attempt_count = Attempt.objects.count()
        attempt_answer_count = AttemptAnswer.objects.count()
        
        self.stdout.write(f'Exams: {exam_count}')
        self.stdout.write(f'Sections: {section_count}')
        self.stdout.write(f'Questions: {question_count}')
        self.stdout.write(f'Attempts: {attempt_count}')
        self.stdout.write(f'Attempt Answers: {attempt_answer_count}')
        self.stdout.write(f'\nTotal records to delete: {exam_count + section_count + question_count + attempt_count + attempt_answer_count}\n')

        # Confirmation prompt
        if not options['no_input']:
            self.stdout.write(self.style.ERROR(
                '\n⚠️  WARNING: This will DELETE ALL data from the following tables:'
            ))
            self.stdout.write('  - exams')
            self.stdout.write('  - sections')
            self.stdout.write('  - questions')
            self.stdout.write('  - attempts')
            self.stdout.write('  - attempt_answers')
            self.stdout.write(self.style.ERROR('\nThis operation CANNOT be undone!\n'))
            
            confirm = input('Type "DELETE ALL" to confirm: ')
            if confirm != 'DELETE ALL':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        # Perform deletion in a transaction
        try:
            with transaction.atomic():
                self.stdout.write(self.style.WARNING('\n=== Starting Deletion ==='))
                
                # Delete in reverse dependency order for better logging
                # (Django will handle CASCADE automatically, but this gives us counts)
                
                self.stdout.write('Deleting AttemptAnswers...')
                deleted_attempt_answers = AttemptAnswer.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {deleted_attempt_answers[0]} AttemptAnswer records'))
                
                self.stdout.write('Deleting Attempts...')
                deleted_attempts = Attempt.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {deleted_attempts[0]} Attempt records'))
                
                self.stdout.write('Deleting Questions...')
                deleted_questions = Question.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {deleted_questions[0]} Question records'))
                
                self.stdout.write('Deleting Sections...')
                deleted_sections = Section.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {deleted_sections[0]} Section records'))
                
                self.stdout.write('Deleting Exams...')
                deleted_exams = Exam.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted {deleted_exams[0]} Exam records'))

            # Verify all tables are empty
            self.stdout.write(self.style.WARNING('\n=== Verifying Database State ==='))
            final_exam_count = Exam.objects.count()
            final_section_count = Section.objects.count()
            final_question_count = Question.objects.count()
            final_attempt_count = Attempt.objects.count()
            final_attempt_answer_count = AttemptAnswer.objects.count()
            
            self.stdout.write(f'Exams: {final_exam_count}')
            self.stdout.write(f'Sections: {final_section_count}')
            self.stdout.write(f'Questions: {final_question_count}')
            self.stdout.write(f'Attempts: {final_attempt_count}')
            self.stdout.write(f'Attempt Answers: {final_attempt_answer_count}')
            
            if all(count == 0 for count in [final_exam_count, final_section_count, 
                                            final_question_count, final_attempt_count, 
                                            final_attempt_answer_count]):
                self.stdout.write(self.style.SUCCESS('\n✅ All data successfully deleted. Database is clean!'))
            else:
                self.stdout.write(self.style.ERROR('\n❌ Warning: Some records may still exist!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error during deletion: {str(e)}'))
            self.stdout.write(self.style.ERROR('Transaction rolled back. No data was deleted.'))
            raise
