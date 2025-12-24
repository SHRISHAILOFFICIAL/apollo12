import PyPDF2
import sys

# Open and read the PDF
pdf_path = 'DCET-2025.pdf'
pdf_reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total pages: {len(pdf_reader.pages)}\n")

# Extract text from all pages
for i in range(len(pdf_reader.pages)):
    print(f"\n{'='*80}")
    print(f"PAGE {i+1}")
    print('='*80)
    text = pdf_reader.pages[i].extract_text()
    print(text)
