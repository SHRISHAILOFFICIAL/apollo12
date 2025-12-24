import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Exam

# Add video solution URL to 2023 DCET exam
try:
    exam = Exam.objects.get(year=2023, name='DCET')
    exam.solution_video_url = 'https://youtu.be/VOD3-Ev0ntk'
    exam.save()
    print(f"✅ Added video solution URL to {exam.name} {exam.year}")
    print(f"   Video URL: {exam.solution_video_url}")
except Exam.DoesNotExist:
    print("❌ DCET 2023 exam not found")
    print("   Available exams:")
    for exam in Exam.objects.all():
        print(f"   - {exam.name} {exam.year}")
