"""
Check DCET 2025 exam status and verify configuration
"""
from exams.models import Exam

print("="*70)
print("🔍 CHECKING DCET EXAMS STATUS")
print("="*70)

# Get all DCET exams
dcet_exams = Exam.objects.filter(name="DCET").order_by('year')

for exam in dcet_exams:
    print(f"\n📋 {exam.name} {exam.year}")
    print(f"   {'─'*60}")
    print(f"   ✓ Published: {exam.is_published}")
    print(f"   ✓ Access Tier: {exam.access_tier}")
    print(f"   ✓ Total Marks: {exam.total_marks}")
    print(f"   ✓ Duration: {exam.duration_minutes} minutes")
    print(f"   ✓ Sections: {exam.sections.count()}")
    
    # Count questions
    total_questions = 0
    for section in exam.sections.all():
        q_count = section.questions.count()
        total_questions += q_count
        print(f"      - {section.name}: {q_count} questions")
    
    print(f"   ✓ Total Questions: {total_questions}")
    
    # Check if accessible
    if exam.access_tier == 'FREE':
        print(f"   🔓 Accessible to: ALL USERS (Free + Pro)")
    else:
        print(f"   🔒 Accessible to: PRO USERS ONLY")

print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

exam_2023 = Exam.objects.filter(name="DCET", year=2023).first()
exam_2025 = Exam.objects.filter(name="DCET", year=2025).first()

if exam_2023:
    print(f"\n✅ DCET 2023: {exam_2023.access_tier} tier - Published: {exam_2023.is_published}")
else:
    print("\n❌ DCET 2023: NOT FOUND")

if exam_2025:
    print(f"✅ DCET 2025: {exam_2025.access_tier} tier - Published: {exam_2025.is_published}")
    
    # Verify all questions are imported
    expected_questions = 100
    actual_questions = sum(s.questions.count() for s in exam_2025.sections.all())
    
    if actual_questions == expected_questions:
        print(f"✅ All {expected_questions} questions imported successfully!")
    else:
        print(f"⚠️  Expected {expected_questions} questions, found {actual_questions}")
else:
    print("❌ DCET 2025: NOT FOUND")

print("\n" + "="*70)
print("🎉 VERIFICATION COMPLETE")
print("="*70)
