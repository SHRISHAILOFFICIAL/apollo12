# Batch Import Script for Math Mock Tests
# Run this script to import all 10 mock tests at once

Write-Host "📚 Starting batch import of Math Mock Tests..." -ForegroundColor Green
Write-Host ""

$mockTests = 1..10

foreach ($i in $mockTests) {
    Write-Host "Importing Mock Test $i..." -ForegroundColor Cyan
    python manage.py import_questions_csv "Math Mock Test" $i "math_mock_tests\mock$i.csv" --duration 15
    Write-Host ""
}

Write-Host "✅ All mock tests imported successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 To publish these exams, run:" -ForegroundColor Yellow
Write-Host "   python manage.py shell" -ForegroundColor White
Write-Host "   >>> from exams.models import Exam" -ForegroundColor White
Write-Host "   >>> exams = Exam.objects.filter(name='Math Mock Test')" -ForegroundColor White
Write-Host "   >>> for exam in exams:" -ForegroundColor White
Write-Host "   ...     exam.is_published = True" -ForegroundColor White
Write-Host "   ...     exam.access_tier = 'PRO'  # or 'FREE'" -ForegroundColor White
Write-Host "   ...     exam.save()" -ForegroundColor White
