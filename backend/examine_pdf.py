import PyPDF2
import re

# Open and read the PDF
pdf_path = 'DCET-2025.pdf'
pdf_reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total pages: {len(pdf_reader.pages)}\n")

# Extract text from first few pages to understand the pattern
for i in range(min(5, len(pdf_reader.pages))):
    print(f"\n{'='*80}")
    print(f"PAGE {i+1}")
    print('='*80)
    text = pdf_reader.pages[i].extract_text()
    print(text[:2000])  # Print first 2000 characters
    print("\n... (truncated)")
