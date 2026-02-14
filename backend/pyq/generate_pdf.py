"""
Generate DCET 2023 PYQ PDF (Questions Only) with a fresh design using fpdf2.
Run: python pyq/generate_pdf.py
"""
import csv
import os
import sys

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fpdf import FPDF

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dcet_pyq_2023.csv')
OUTPUT_PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DCET_2023_PYQ_Questions.pdf')


class PYQDocument(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(True, margin=15)
        
    def header(self):
        if self.page_no() == 1:
            return  # Custom header on first page
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, 'DCET 2023 - Previous Year Questions', align='C')
        self.ln(8)
        self.set_draw_color(79, 70, 229)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f'Page {self.page_no()}/{{nb}}', align='C')

    def draw_title_page(self):
        self.add_page()
        self.ln(40)
        
        # Purple accent bar
        self.set_fill_color(79, 70, 229)
        self.rect(20, 55, 170, 3, 'F')
        
        self.ln(25)
        self.set_font('Helvetica', 'B', 32)
        self.set_text_color(49, 46, 129)
        self.cell(0, 14, 'DCET 2023', align='C')
        self.ln(16)
        
        self.set_font('Helvetica', '', 14)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, 'Diploma Common Entrance Test', align='C')
        self.ln(12)
        
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(79, 70, 229)
        self.cell(0, 8, 'Previous Year Questions', align='C')
        self.ln(16)
        
        # Badge
        badge_w = 80
        badge_x = (210 - badge_w) / 2
        self.set_fill_color(79, 70, 229)
        self.set_draw_color(79, 70, 229)
        self.rect(badge_x, self.get_y(), badge_w, 10, 'F')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(badge_x, self.get_y())
        self.cell(badge_w, 10, 'QUESTIONS ONLY  |  PRACTICE PAPER', align='C')
        self.ln(20)
        
        # Info box
        self.set_fill_color(248, 250, 252)
        self.set_draw_color(226, 232, 240)
        self.rect(30, self.get_y(), 150, 30, 'DF')
        
        y_info = self.get_y() + 5
        self.set_font('Helvetica', '', 10)
        self.set_text_color(71, 85, 105)
        
        info_items = [
            'Total Questions: 100  |  Maximum Marks: 100',
            'Duration: 3 Hours  |  Each Question: 1 Mark',
            'Sections: 6 (IT, EEE, Project Mgmt, Maths, Stats)'
        ]
        for item in info_items:
            self.set_xy(30, y_info)
            self.cell(150, 7, item, align='C')
            y_info += 8
        
        self.ln(40)
        
        # Bottom accent bar
        self.set_fill_color(79, 70, 229)
        self.rect(20, self.get_y(), 170, 3, 'F')
        
        self.ln(15)
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6, 'For Practice Purpose Only  |  apollo12', align='C')

    def draw_section_header(self, name, color):
        # Check if there's enough space
        if self.get_y() > 260:
            self.add_page()
        
        self.ln(4)
        r, g, b = color
        self.set_fill_color(r, g, b)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f'  {name.upper()}', fill=True)
        self.ln(6)

    def draw_question(self, qnum, qtext, options, accent_color):
        r, g, b = accent_color
        
        # Clean up text - remove LaTeX
        qtext = clean_text(qtext)
        opts_clean = [clean_text(o) for o in options]
        
        # Estimate height needed
        self.set_font('Helvetica', '', 9)
        text_lines = self.multi_cell(170, 5, qtext, dry_run=True, output="LINES")
        estimated_h = 8 + len(text_lines) * 5 + 24
        
        if self.get_y() + estimated_h > 275:
            self.add_page()
        
        start_y = self.get_y()
        
        # Left accent bar
        self.set_fill_color(r, g, b)
        self.rect(12, start_y, 2, 2, 'F')
        
        # Question number
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(r, g, b)
        self.set_x(16)
        self.cell(12, 5, f'Q{qnum}.')
        
        # Question text
        self.set_font('Helvetica', '', 9)
        self.set_text_color(30, 41, 59)
        self.set_x(28)
        self.multi_cell(170, 5, qtext)
        self.ln(1)
        
        # Options in 2x2 grid
        labels = ['(A)', '(B)', '(C)', '(D)']
        col_w = 85
        start_x = 28
        
        for i, (label, opt) in enumerate(zip(labels, opts_clean)):
            col = i % 2
            if i == 0 or i == 2:
                opt_y = self.get_y()
            
            x = start_x + col * col_w
            self.set_xy(x, opt_y)
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(r, g, b)
            self.cell(8, 5, label)
            self.set_font('Helvetica', '', 8)
            self.set_text_color(51, 65, 85)
            self.cell(col_w - 10, 5, opt[:50])
            
            if col == 1 or i == 3:
                self.ln(5)
        
        self.ln(3)
        
        # Separator line
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.2)
        self.line(16, self.get_y(), 195, self.get_y())
        self.ln(3)


def clean_text(text):
    """Remove LaTeX markup for plain PDF rendering"""
    import re
    text = re.sub(r'\\[({}\[\])]', '', text)
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\1/\2', text)
    text = re.sub(r'\\(Omega|omega)', 'Ohm', text)
    text = re.sub(r'\\(pi)', 'pi', text)
    text = re.sub(r'\\(sqrt)\{([^}]*)\}', r'sqrt(\2)', text)
    text = re.sub(r'\\begin\{[^}]*\}', '', text)
    text = re.sub(r'\\end\{[^}]*\}', '', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'[{}$\\]', '', text)
    # Replace remaining Unicode with ASCII
    text = text.replace('\u03a9', 'Ohm')
    text = text.replace('\u03c0', 'pi')
    text = text.replace('\u221a', 'sqrt')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2014', '-')
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    # Remove any non-ASCII
    text = text.encode('ascii', 'replace').decode('ascii')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    # Read CSV
    questions = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('question_number'):
                questions.append(row)

    # Group by section
    sections = {}
    for q in questions:
        sec = q['section_name'].strip()
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(q)

    # Section colors (R, G, B)
    section_colors = [
        (79, 70, 229),    # Indigo
        (8, 145, 178),    # Cyan
        (5, 150, 105),    # Green
        (217, 119, 6),    # Amber
        (220, 38, 38),    # Red
        (124, 58, 237),   # Purple
    ]

    # Create PDF
    pdf = PYQDocument()
    pdf.alias_nb_pages()
    
    # Title page
    pdf.draw_title_page()
    
    # Add new page for questions
    pdf.add_page()
    
    for idx, (sec_name, sec_qs) in enumerate(sections.items()):
        color = section_colors[idx % len(section_colors)]
        pdf.draw_section_header(sec_name, color)
        
        for q in sec_qs:
            opts = [
                q.get('option_a', ''),
                q.get('option_b', ''),
                q.get('option_c', ''),
                q.get('option_d', ''),
            ]
            pdf.draw_question(q['question_number'], q.get('plain_text', q['question_text']), opts, color)
    
    pdf.output(OUTPUT_PDF)
    print(f"PDF generated: {OUTPUT_PDF}")
    print(f"Total questions: {len(questions)}")
    print(f"File size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")


if __name__ == '__main__':
    main()
