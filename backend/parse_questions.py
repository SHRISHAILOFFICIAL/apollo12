import PyPDF2
import re
import csv

def extract_all_text(pdf_path):
    """Extract all text from PDF"""
    pdf_reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

def parse_questions(text):
    """Parse questions from extracted text"""
    questions = []
    
    # Pattern to match question numbers (1., 2., etc.)
    # This will help us identify where questions start
    lines = text.split('\n')
    
    current_question = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line starts with a question number (1. to 100.)
        match = re.match(r'^(\d{1,3})\.?\s+(.+)', line)
        if match:
            q_num = int(match.group(1))
            if 1 <= q_num <= 100:
                # Save previous question if exists
                if current_question:
                    questions.append({
                        'number': current_question,
                        'text': ' '.join(current_text)
                    })
                
                # Start new question
                current_question = q_num
                current_text = [match.group(2)]
                continue
        
        # Add to current question text
        if current_question:
            current_text.append(line)
    
    # Add last question
    if current_question:
        questions.append({
            'number': current_question,
            'text': ' '.join(current_text)
        })
    
    return questions

# Extract text
print("📖 Reading PDF...")
pdf_path = 'DCET-2025.pdf'
text = extract_all_text(pdf_path)

# Save extracted text for manual review
with open('extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("✅ Saved extracted text to 'extracted_text.txt'")

# Parse questions
print("\n🔍 Parsing questions...")
questions = parse_questions(text)

print(f"\n✅ Found {len(questions)} potential questions")
print("\nFirst 5 questions:")
for q in questions[:5]:
    print(f"\nQ{q['number']}: {q['text'][:200]}...")

print("\n" + "="*80)
print("📝 Next step: Review 'extracted_text.txt' to understand the pattern")
print("   Then we'll create a proper parser to extract questions and options")
