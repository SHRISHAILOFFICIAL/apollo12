import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Question
from django.core.cache import cache

# Update Q99
q99 = Question.objects.filter(
    section__exam__name='DCET', 
    section__exam__year=2023, 
    question_number=99
).first()

if q99:
    q99.option_a = "(' ')"
    q99.option_b = '(" ")'
    q99.option_c = '( )'
    q99.option_d = '(""" """)'
    q99.save()
    
    print("✅ Q99 updated in database:")
    print(f"  A: {q99.option_a}")
    print(f"  B: {q99.option_b}")
    print(f"  C: {q99.option_c}")
    print(f"  D: {q99.option_d}")
    
    # Clear cache
    cache.clear()
    print("✅ Cache cleared")
else:
    print("❌ Q99 not found")
