# DCET 2025 Question Import Guide

## Problem
The PDF `DCET-2025.pdf` contains scanned images, not extractable text.

## Solutions

### Option 1: Use Online OCR (Recommended - Fastest)
1. Go to https://www.onlineocr.net/ or https://www.adobe.com/acrobat/online/pdf-to-text.html
2. Upload `DCET-2025.pdf`
3. Download the extracted text
4. Copy-paste questions into `dcet_pyq_2025.csv`

### Option 2: Use Google Drive OCR (Most Accurate)
1. Upload PDF to Google Drive
2. Right-click → Open with → Google Docs
3. Google will automatically OCR the PDF
4. Copy the text and fill in the CSV

### Option 3: Manual Entry (Most Reliable)
1. Open `DCET-2025.pdf` in one window
2. Open `dcet_pyq_2025.csv` in Excel/VS Code
3. Manually type in questions, options, and answers
4. This ensures 100% accuracy

### Option 4: Use AI to Help (ChatGPT/Claude)
1. Take screenshots of each page
2. Upload to ChatGPT/Claude and ask it to extract questions
3. Copy the output into the CSV

### Option 5: Install Tesseract OCR (Technical)
If you want to use OCR locally:
```bash
# Download and install Tesseract from:
# https://github.com/UB-Mannheim/tesseract/wiki

# Then run:
pip install pytesseract pdf2image
python ocr_extract.py
```

## CSV Format Reminder
```csv
section_name,question_number,question_text,plain_text,option_a,option_b,option_c,option_d,correct_option,marks,diagram_url
ENGINEERING MATHEMATICS,1,"Question with LaTeX \( x^2 \)","Question without LaTeX","Option A","Option B","Option C","Option D",A,1,
```

## After Filling CSV
Import with:
```bash
python manage.py import_questions_csv "DCET" 2025 dcet_pyq_2025.csv
```

## Section Breakdown
- **ENGINEERING MATHEMATICS**: Q1-Q20
- **STATISTICS & ANALYTICS**: Q21-Q40
- **IT Skills**: Q41-Q60
- **FUNDAMENTALS OF ELECTRICAL & ELECTRONICS ENGINEERING**: Q61-Q80
- **PROJECT MANAGEMENT SKILLS**: Q81-Q100
