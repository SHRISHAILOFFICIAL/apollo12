"""
Setup script to add Notes and PYQ records to the database.
Run on the VM after migrations:
  source venv/bin/activate
  python manage.py migrate
  python setup_notes_pyqs.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from exams.models import Note, PYQ

# ─── NOTES ───────────────────────────────────────────────
notes_data = [
    {
        'subject': 'Engineering Mathematics',
        'topic': 'Matrices',
        'description': 'Complete notes on Matrices - types, operations, determinants, inverse and eigenvalues',
        'file_path': 'engineering_Mathematics/matrix_notes.pdf',
        'access_tier': 'FREE',
        'order': 1,
    },
]

print("=== Setting up Notes ===")
for data in notes_data:
    note, created = Note.objects.update_or_create(
        subject=data['subject'],
        topic=data['topic'],
        defaults={
            'description': data['description'],
            'file_path': data['file_path'],
            'access_tier': data['access_tier'],
            'is_active': True,
            'order': data['order'],
        }
    )
    action = 'Created' if created else 'Updated'
    print(f"  {action}: {note} (id={note.id}, tier={note.access_tier})")

# ─── PYQs ────────────────────────────────────────────────
pyqs_data = [
    {
        'exam_name': 'DCET 2023',
        'year': 2023,
        'description': 'DCET 2023 PYQ - 100 MCQs (Questions Only)',
        'file_path': 'DCET_2023_PYQ_Questions.pdf',
        'access_tier': 'FREE',
        'order': 1,
    },
]

print("\n=== Setting up PYQs ===")
for data in pyqs_data:
    pyq, created = PYQ.objects.update_or_create(
        exam_name=data['exam_name'],
        year=data['year'],
        defaults={
            'description': data['description'],
            'file_path': data['file_path'],
            'access_tier': data['access_tier'],
            'is_active': True,
            'order': data['order'],
        }
    )
    action = 'Created' if created else 'Updated'
    print(f"  {action}: {pyq} (id={pyq.id}, tier={pyq.access_tier})")

# ─── Verify files exist ─────────────────────────────────
from django.conf import settings

print("\n=== Verifying files ===")
notes_root = os.path.join(settings.BASE_DIR, 'notes')
pyq_root = os.path.join(settings.BASE_DIR, 'pyq')

for note in Note.objects.filter(is_active=True):
    path = os.path.join(notes_root, note.file_path)
    exists = '✓' if os.path.exists(path) else '✗ MISSING'
    print(f"  Note: {path} [{exists}]")

for pyq in PYQ.objects.filter(is_active=True):
    path = os.path.join(pyq_root, pyq.file_path)
    exists = '✓' if os.path.exists(path) else '✗ MISSING'
    print(f"  PYQ:  {path} [{exists}]")

print("\nDone!")
