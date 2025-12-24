# Math Mock Tests - Import Guide

## 📁 Folder Structure

```
math_mock_tests/
├── mock1.csv   (4 questions - Matrices & Determinants)
├── mock2.csv   (4 questions - Matrix Operations)
├── mock3.csv   (4 questions - Determinants & Theory)
├── mock4.csv   (4 questions - Determinant Properties)
├── mock5.csv   (4 questions - Identity & Diagonal Matrices)
├── mock6.csv   (4 questions - Matrix Multiplication & Eigenvalues)
├── mock7.csv   (4 questions - Symmetric Matrices)
├── mock8.csv   (4 questions - Eigenvalues & Linear Systems)
├── mock9.csv   (4 questions - Scalar Multiplication)
└── mock10.csv  (4 questions - Matrix Types)
```

## 🚀 Quick Import (All at Once)

Run the batch import script:

```powershell
cd backend
.\import_math_mocks.ps1
```

## 📝 Manual Import (One by One)

Import individual mock tests:

```bash
cd backend

# Mock Test 1
python manage.py import_questions_csv "Math Mock Test" 1 math_mock_tests\mock1.csv --duration 15

# Mock Test 2
python manage.py import_questions_csv "Math Mock Test" 2 math_mock_tests\mock2.csv --duration 15

# ... and so on for mock3.csv to mock10.csv
```

## ✅ Publish Exams

After importing, publish the exams:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from exams.models import Exam

# Get all Math Mock Tests
exams = Exam.objects.filter(name='Math Mock Test')

# Publish all and set access tier
for exam in exams:
    exam.is_published = True
    exam.access_tier = 'PRO'  # or 'FREE'
    exam.save()
    print(f"Published: {exam}")
```

## 📊 Verify Import

Check that all exams were imported correctly:

```python
from exams.models import Exam, Question

# List all Math Mock Tests
exams = Exam.objects.filter(name='Math Mock Test').order_by('year')
for exam in exams:
    q_count = Question.objects.filter(section__exam=exam).count()
    print(f"{exam} - {q_count} questions")
```

Expected output:
```
Math Mock Test 1 - 4 questions
Math Mock Test 2 - 4 questions
...
Math Mock Test 10 - 4 questions
```

## 📋 CSV Format

Each CSV file follows this format:

```csv
section_name,question_number,question_text,plain_text,option_a,option_b,option_c,option_d,correct_option,marks,diagram_url
ENGINEERING MATHEMATICS,1,"$\text{Question with LaTeX}$","Plain text version",...
```

## 🎯 Topics Covered

- Matrix operations (addition, subtraction, multiplication)
- Determinants (2×2 and 3×3)
- Matrix inverse and adjoint
- Eigenvalues and eigenvectors
- Characteristic equations
- Cramer's rule
- Matrix types (identity, diagonal, scalar, triangular, symmetric)
- Linear systems of equations
