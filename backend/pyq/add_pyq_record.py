"""
Add/update the DCET 2023 PYQ record in the database.
Run: python manage.py shell < pyq/add_pyq_record.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import PYQ

# Create or update the PYQ record
pyq, created = PYQ.objects.update_or_create(
    exam_name='DCET 2023',
    year=2023,
    defaults={
        'description': 'DCET 2023 Previous Year Questions - 100 MCQs (Questions Only)',
        'file_path': 'DCET_2023_PYQ_Questions.pdf',
        'access_tier': 'FREE',
        'is_active': True,
        'order': 1,
    }
)

action = 'Created' if created else 'Updated'
print(f"{action} PYQ record: {pyq}")
print(f"  ID: {pyq.id}")
print(f"  File: {pyq.file_path}")
print(f"  Tier: {pyq.access_tier}")
print(f"  Active: {pyq.is_active}")
