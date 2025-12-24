"""
Script to help create CSV from DCET 2025 PDF
This will create a template CSV that you can fill in by reading the PDF
"""
import csv

# Section mapping based on user's description
sections = [
    ("ENGINEERING MATHEMATICS", 1, 20),      # Questions 1-20
    ("STATISTICS & ANALYTICS", 21, 40),      # Questions 21-40
    ("IT Skills", 41, 60),                   # Questions 41-60
    ("FUNDAMENTALS OF ELECTRICAL & ELECTRONICS ENGINEERING", 61, 80),  # Questions 61-80
    ("PROJECT MANAGEMENT SKILLS", 81, 100),  # Questions 81-100
]

# Create CSV file
csv_file = 'dcet_pyq_2025.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
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
    
    # Create template rows for each question
    for section_name, start_q, end_q in sections:
        for q_num in range(start_q, end_q + 1):
            writer.writerow([
                section_name,
                q_num,
                '',  # question_text - TO BE FILLED
                '',  # plain_text - TO BE FILLED
                '',  # option_a - TO BE FILLED
                '',  # option_b - TO BE FILLED
                '',  # option_c - TO BE FILLED
                '',  # option_d - TO BE FILLED
                '',  # correct_option - TO BE FILLED (A/B/C/D)
                '1', # marks - default 1
                ''   # diagram_url - leave empty
            ])

print(f"✅ Created template CSV: {csv_file}")
print(f"📝 Total questions: 100")
print(f"📁 Sections: {len(sections)}")
print("\nNow you need to:")
print("1. Open the PDF: DCET-2025.pdf")
print("2. Open the CSV: dcet_pyq_2025.csv")
print("3. Fill in the questions, options, and correct answers")
print("\nSection breakdown:")
for section_name, start_q, end_q in sections:
    print(f"  • {section_name}: Q{start_q}-Q{end_q}")
