import csv

# Read CSV
csv_file = 'dcet_pyq_2023.csv'

# HTML template with fixed layout and proper LaTeX handling
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DCET 2023 Question Paper</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        @page {
            size: A4;
            margin: 15mm;
        }
        
        @media print {
            .no-print { display: none !important; }
            body { 
                font-size: 9pt;
                margin: 0;
                padding: 0;
            }
            .page {
                page-break-after: always;
                margin: 0;
            }
            .question {
                page-break-inside: avoid;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.35;
            background: #f5f5f5;
        }
        
        .page {
            width: 210mm;
            min-height: 297mm;
            margin: 10mm auto;
            background: white;
            border: 3px solid #000;
            padding: 10mm;
        }
        
        .header {
            text-align: center;
            border-bottom: 2px solid #000;
            padding-bottom: 8px;
            margin-bottom: 10px;
        }
        
        h1 {
            font-size: 22pt;
            margin: 4px 0;
        }
        
        h2 {
            font-size: 13pt;
            margin: 3px 0;
        }
        
        .instructions {
            border: 1px solid #000;
            padding: 6px;
            margin-bottom: 10px;
            font-size: 8.5pt;
        }
        
        .instructions ul {
            margin-left: 18px;
            margin-top: 3px;
        }
        
        .section-title {
            background: #000;
            color: white;
            padding: 5px 8px;
            font-size: 10pt;
            font-weight: bold;
            margin: 10px 0 6px 0;
            text-align: center;
        }
        
        .questions-container {
            display: flex;
            gap: 0;
        }
        
        .column-left {
            flex: 1;
            padding-right: 6px;
        }
        
        .column-divider {
            width: 2px;
            background: #000;
            flex-shrink: 0;
        }
        
        .column-right {
            flex: 1;
            padding-left: 6px;
        }
        
        .question {
            border: 1.5px solid #333;
            padding: 6px;
            margin-bottom: 6px;
            background: white;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }
        
        .question-number {
            font-weight: bold;
            margin-bottom: 3px;
            font-size: 9pt;
        }
        
        .question-text {
            margin-bottom: 4px;
            line-height: 1.3;
        }
        
        .options {
            margin-left: 4px;
        }
        
        .option {
            margin: 1.5px 0;
            line-height: 1.25;
        }
        
        .answer-key-page {
            width: 210mm;
            min-height: 297mm;
            margin: 10mm auto;
            background: white;
            border: 3px solid #000;
            padding: 12mm;
        }
        
        .answer-key-title {
            text-align: center;
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #000;
        }
        
        .answer-grid {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 4px;
        }
        
        .answer-item {
            border: 1px solid #666;
            padding: 3px;
            text-align: center;
            font-size: 8.5pt;
        }
        
        .answer-number {
            font-weight: bold;
        }
        
        .answer-value {
            color: #006400;
            font-weight: bold;
        }
        
        .no-print {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2196F3;
            color: white;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            z-index: 1000;
            font-size: 14pt;
            border: none;
            font-weight: bold;
        }
        
        .no-print:hover {
            background: #1976D2;
        }
    </style>
</head>
<body>
    <button class="no-print" onclick="window.print()">🖨️ Print to PDF</button>
    
    <div class="page">
        <div class="header">
            <h1>DCET 2023</h1>
            <h2>Diploma Common Entrance Test</h2>
            <p><strong>Question Paper</strong></p>
        </div>
        
        <div class="instructions">
            <strong>Instructions:</strong>
            <ul>
                <li>Total Questions: 100 | Maximum Marks: 100 | Duration: 3 hours</li>
                <li>Each question carries 1 mark | Answer key provided at the end</li>
            </ul>
        </div>
'''

# Read CSV and organize by sections
sections = {}
all_answers = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        section = row['section_name'].strip()
        if not section:
            continue
        if section not in sections:
            sections[section] = []
        sections[section].append(row)

def clean_text(text):
    """Remove LaTeX escape characters for plain display"""
    # Replace common LaTeX escapes
    text = text.replace('\\_', '_')  # Underscores
    text = text.replace('\\textbf{', '').replace('}', '')  # Bold
    # Keep math mode delimiters for MathJax
    return text

# Generate questions by section with two-column layout
for section_name, questions in sections.items():
    if not section_name:
        continue
    
    html_content += f'<div class="section-title">{section_name}</div>\n'
    html_content += '<div class="questions-container">\n'
    
    # Split questions into left and right columns
    mid = (len(questions) + 1) // 2
    left_questions = questions[:mid]
    right_questions = questions[mid:]
    
    # Left column
    html_content += '<div class="column-left">\n'
    for q in left_questions:
        q_num = q['question_number']
        q_text = clean_text(q['question_text'].strip())
        opt_a = clean_text(q['option_a'].strip())
        opt_b = clean_text(q['option_b'].strip())
        opt_c = clean_text(q['option_c'].strip())
        opt_d = clean_text(q['option_d'].strip())
        correct = q['correct_option'].strip()
        
        all_answers.append((q_num, correct))
        
        html_content += '<div class="question">\n'
        html_content += f'<div class="question-number">Q{q_num}.</div>\n'
        html_content += f'<div class="question-text">{q_text}</div>\n'
        html_content += '<div class="options">\n'
        html_content += f'<div class="option">(A) {opt_a}</div>\n'
        html_content += f'<div class="option">(B) {opt_b}</div>\n'
        html_content += f'<div class="option">(C) {opt_c}</div>\n'
        html_content += f'<div class="option">(D) {opt_d}</div>\n'
        html_content += '</div>\n'
        html_content += '</div>\n\n'
    html_content += '</div>\n'
    
    # Divider
    html_content += '<div class="column-divider"></div>\n'
    
    # Right column
    html_content += '<div class="column-right">\n'
    for q in right_questions:
        q_num = q['question_number']
        q_text = clean_text(q['question_text'].strip())
        opt_a = clean_text(q['option_a'].strip())
        opt_b = clean_text(q['option_b'].strip())
        opt_c = clean_text(q['option_c'].strip())
        opt_d = clean_text(q['option_d'].strip())
        correct = q['correct_option'].strip()
        
        all_answers.append((q_num, correct))
        
        html_content += '<div class="question">\n'
        html_content += f'<div class="question-number">Q{q_num}.</div>\n'
        html_content += f'<div class="question-text">{q_text}</div>\n'
        html_content += '<div class="options">\n'
        html_content += f'<div class="option">(A) {opt_a}</div>\n'
        html_content += f'<div class="option">(B) {opt_b}</div>\n'
        html_content += f'<div class="option">(C) {opt_c}</div>\n'
        html_content += f'<div class="option">(D) {opt_d}</div>\n'
        html_content += '</div>\n'
        html_content += '</div>\n\n'
    html_content += '</div>\n'
    
    html_content += '</div>\n\n'

html_content += '</div>\n\n'  # Close page div

# Add answer key section
html_content += '''
<div class="answer-key-page">
    <div class="answer-key-title">ANSWER KEY</div>
    <div class="answer-grid">
'''

# Sort answers by question number
all_answers.sort(key=lambda x: int(x[0]))

for q_num, answer in all_answers:
    html_content += f'''
        <div class="answer-item">
            <span class="answer-number">{q_num}.</span>
            <span class="answer-value">({answer})</span>
        </div>
'''

html_content += '''
    </div>
</div>
'''

html_content += '''
</body>
</html>
'''

# Write HTML file
with open('dcet_2023_question_paper.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ Fixed question paper created with:")
print("  - Proper page breaks (no cut-off questions)")
print("  - Fixed alignment")
print("  - Removed backslashes (cleaned LaTeX escapes)")
print("  - Individual question boxes")
print("  - Page border and vertical partition")
print("  - Answer key at the end")
print("\nFile: dcet_2023_question_paper.html")
print("\nIMPORTANT: When printing to PDF:")
print("  1. Press Ctrl+P")
print("  2. Set 'Margins' to 'None' or 'Minimum'")
print("  3. Enable 'Background graphics'")
print("  4. Save as PDF")
