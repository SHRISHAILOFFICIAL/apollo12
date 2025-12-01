import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Test, Question

def populate():
    if Test.objects.count() > 0:
        print("Tests already exist.")
        return

    for i in range(1, 6):
        test = Test.objects.create(
            title=f"DCET Mock Test {i}",
            description=f"This is a mock test for DCET preparation. Test number {i}.",
            duration=120,
            total_marks=100,
            is_published=True
        )
        print(f"Created {test.title}")
        
        # Add dummy questions
        for q in range(1, 21): # 20 questions per test for now
            Question.objects.create(
                test=test,
                text=f"Question {q} for Test {i}: What is the capital of Karnataka?",
                option_a="Bengaluru",
                option_b="Mysuru",
                option_c="Hubballi",
                option_d="Mangaluru",
                correct_option="A",
                marks=1
            )

if __name__ == "__main__":
    populate()
