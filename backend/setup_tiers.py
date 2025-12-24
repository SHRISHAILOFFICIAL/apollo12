from exams.models import Exam

# Get the exams
exam_2023 = Exam.objects.get(name="DCET", year=2023)
exam_2025 = Exam.objects.get(name="DCET", year=2025)

# Configure DCET 2023 as FREE
exam_2023.access_tier = 'FREE'
exam_2023.is_published = True
exam_2023.save()

# Configure DCET 2025 as PRO
exam_2025.access_tier = 'PRO'
exam_2025.is_published = True
exam_2025.save()

print("="*60)
print("✅ Access tiers configured successfully!")
print("="*60)
print(f"\n📝 DCET 2023:")
print(f"   Access Tier: {exam_2023.access_tier}")
print(f"   Published: {exam_2023.is_published}")
print(f"   Total Marks: {exam_2023.total_marks}")
print(f"   Duration: {exam_2023.duration_minutes} minutes")
print(f"   Sections: {exam_2023.sections.count()}")
print(f"   Questions: {sum(s.questions.count() for s in exam_2023.sections.all())}")

print(f"\n📝 DCET 2025:")
print(f"   Access Tier: {exam_2025.access_tier}")
print(f"   Published: {exam_2025.is_published}")
print(f"   Total Marks: {exam_2025.total_marks}")
print(f"   Duration: {exam_2025.duration_minutes} minutes")
print(f"   Sections: {exam_2025.sections.count()}")
print(f"   Questions: {sum(s.questions.count() for s in exam_2025.sections.all())}")

print("\n" + "="*60)
print("🎉 Configuration Complete!")
print("="*60)
print("\n✅ FREE users can access: DCET 2023")
print("🔒 PRO users can access: DCET 2023, DCET 2025")
