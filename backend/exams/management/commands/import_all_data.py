"""
Django management command to batch import all DCET exam data from CSV files.
Usage: python manage.py import_all_data

This imports:
- DCET PYQ 2023 (FREE tier)
- DCET PYQ 2025 (PRO tier)
- Mock Tests 1-4 (PRO tier)

All exams are auto-published after import.
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from payments.models import Plan


class Command(BaseCommand):
    help = 'Import all DCET exam data from CSV files and set up plans'

    def add_arguments(self, parser):
        parser.add_argument(
            '--include-all-mocks',
            action='store_true',
            help='Import all 10 mock tests instead of just 4'
        )

    def handle(self, *args, **options):
        include_all = options['include_all_mocks']
        
        # Find the base directory (where CSVs are stored)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🚀 DCET Platform - Batch Data Import'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # =====================================================
        # Step 1: Create PRO Plan
        # =====================================================
        self.stdout.write(self.style.SUCCESS('\n📋 Step 1: Setting up PRO Plan...'))
        plan, created = Plan.objects.get_or_create(
            key='pro_yearly',
            defaults={
                'name': 'PRO Plan',
                'price_in_paisa': 14900,
                'duration_days': 365,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('   ✅ PRO Plan created (₹149/year)'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️  PRO Plan already exists'))
        
        # =====================================================
        # Step 2: Import PYQ 2023 (FREE)
        # =====================================================
        self.stdout.write(self.style.SUCCESS('\n📋 Step 2: Importing DCET PYQ 2023 (FREE)...'))
        csv_path = os.path.join(base_dir, 'dcet_pyq_2023.csv')
        if os.path.exists(csv_path):
            call_command('import_questions_csv', 'DCET PYQ', '2023', csv_path,
                        access_tier='FREE', publish=True, duration=120)
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ File not found: {csv_path}'))
        
        # =====================================================
        # Step 3: Import PYQ 2025 (PRO)
        # =====================================================
        self.stdout.write(self.style.SUCCESS('\n📋 Step 3: Importing DCET PYQ 2025 (PRO)...'))
        csv_path = os.path.join(base_dir, 'dcet_pyq_2025.csv')
        if os.path.exists(csv_path):
            call_command('import_questions_csv', 'DCET PYQ', '2025', csv_path,
                        access_tier='PRO', publish=True, duration=120)
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ File not found: {csv_path}'))
        
        # =====================================================
        # Step 4: Import Mock Tests (PRO)
        # =====================================================
        mock_count = 10 if include_all else 4
        self.stdout.write(self.style.SUCCESS(f'\n📋 Step 4: Importing Mock Tests 1-{mock_count} (PRO)...'))
        
        mock_dir = os.path.join(base_dir, 'math_mock_tests')
        for i in range(1, mock_count + 1):
            csv_path = os.path.join(mock_dir, f'mock{i}.csv')
            if os.path.exists(csv_path):
                call_command('import_questions_csv', 'Mock Test', str(i), csv_path,
                            access_tier='PRO', publish=True, duration=120)
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ File not found: {csv_path}'))
        
        # =====================================================
        # Summary
        # =====================================================
        from exams.models import Exam, Question
        total_exams = Exam.objects.count()
        total_questions = Question.objects.count()
        free_exams = Exam.objects.filter(access_tier='FREE').count()
        pro_exams = Exam.objects.filter(access_tier='PRO').count()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Import Complete! Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   📊 Total Exams: {total_exams}'))
        self.stdout.write(self.style.SUCCESS(f'   📝 Total Questions: {total_questions}'))
        self.stdout.write(self.style.SUCCESS(f'   🆓 Free Exams: {free_exams}'))
        self.stdout.write(self.style.SUCCESS(f'   🔒 PRO Exams: {pro_exams}'))
        self.stdout.write(self.style.SUCCESS(f'   💰 PRO Plan: ₹{plan.price_in_paisa/100:.0f}/year'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
