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

def clean_text(text):
    """Clean up text formatting"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_questions_from_text(text):
    """Parse questions, options, and answers from text"""
    questions = []
    
    # Split by question numbers (1. to 100.)
    # Pattern: number followed by dot and space
    question_pattern = r'(\d{1,3})\.\s+'
    parts = re.split(question_pattern, text)
    
    # Process each question
    for i in range(1, len(parts), 2):
        if i+1 >= len(parts):
            break
            
        q_num = int(parts[i])
        if not (1 <= q_num <= 100):
            continue
            
        content = parts[i+1]
        
        # Find the answer line (Ans : (a) or similar)
        ans_match = re.search(r'Ans\s*:\s*\(([a-dA-D])\)', content)
        if not ans_match:
            print(f"⚠️  Warning: No answer found for Q{q_num}")
            continue
        
        correct_answer = ans_match.group(1).upper()
        
        # Extract content before the answer (this contains question and options)
        content_before_ans = content[:ans_match.start()]
        
        # Try to find options a), b), c), d)
        option_pattern = r'([a-d])\)\s*([^a-d]+?)(?=[a-d]\)|$)'
        options_matches = list(re.finditer(option_pattern, content_before_ans, re.IGNORECASE))
        
        if len(options_matches) < 4:
            print(f"⚠️  Warning: Found only {len(options_matches)} options for Q{q_num}")
            # Try to continue anyway
        
        # Extract options
        options = {}
        for match in options_matches[:4]:  # Take first 4 options
            opt_letter = match.group(1).lower()
            opt_text = clean_text(match.group(2))
            options[opt_letter] = opt_text
        
        # Extract question text (everything before first option)
        if options_matches:
            question_text = content_before_ans[:options_matches[0].start()]
        else:
            question_text = content_before_ans
        
        question_text = clean_text(question_text)
        
        # Store question data
        questions.append({
            'number': q_num,
            'question': question_text,
            'option_a': options.get('a', ''),
            'option_b': options.get('b', ''),
            'option_c': options.get('c', ''),
            'option_d': options.get('d', ''),
            'correct': correct_answer
        })
    
    return questions

def assign_sections(questions):
    """Assign section names based on question numbers"""
    section_mapping = [
        ("ENGINEERING MATHEMATICS", 1, 20),
        ("STATISTICS & ANALYTICS", 21, 40),
        ("IT Skills", 41, 60),
        ("FUNDAMENTALS OF ELECTRICAL & ELECTRONICS ENGINEERING", 61, 80),
        ("PROJECT MANAGEMENT SKILLS", 81, 100),
    ]
    
    for q in questions:
        q_num = q['number']
        for section_name, start, end in section_mapping:
            if start <= q_num <= end:
                q['section'] = section_name
                break
    
    return questions

def save_to_csv(questions, output_file):
    """Save questions to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow([
            'section_name',
            'question_number',
            'question_text',
            'plain_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
            'marks',
            'diagram_url'
        ])
        
        # Write questions
        for q in sorted(questions, key=lambda x: x['number']):
            writer.writerow([
                q.get('section', ''),
                q['number'],
                q['question'],  # question_text (can add LaTeX later)
                q['question'],  # plain_text (same for now)
                q['option_a'],
                q['option_b'],
                q['option_c'],
                q['option_d'],
                q['correct'],
                1,  # marks
                ''  # diagram_url
            ])

# Main execution
print("📖 Reading PDF...")
text = extract_all_text('DCET-2025.pdf')

print("🔍 Parsing questions...")
questions = parse_questions_from_text(text)

print(f"✅ Parsed {len(questions)} questions")

print("\n📁 Assigning sections...")
questions = assign_sections(questions)

print("\n💾 Saving to CSV...")
save_to_csv(questions, 'dcet_pyq_2025_auto.csv')

print(f"\n✅ SUCCESS! Created 'dcet_pyq_2025_auto.csv' with {len(questions)} questions")

# Show sample
print("\n📋 Sample questions:")
for q in questions[:3]:
    print(f"\nQ{q['number']} ({q.get('section', 'Unknown')})")
    print(f"Question: {q['question'][:80]}...")
    print(f"Options: a) {q['option_a'][:40]}... | Correct: {q['correct']}")

print("\n" + "="*80)
print("🎉 CSV file ready! Review it and then import with:")
print("   python manage.py import_questions_csv \"DCET\" 2025 dcet_pyq_2025_auto.csv")
