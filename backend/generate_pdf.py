import csv
import os

# Read CSV and generate LaTeX document
csv_file = 'dcet_pyq_2023.csv'

# LaTeX preamble
latex_content = r'''\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{xcolor}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textbf{DCET 2023 Question Paper}}
\fancyhead[R]{Page \thepage}
\renewcommand{\headrulewidth}{0.4pt}

\title{\textbf{\Huge DCET 2023}\\[0.5em]\Large Diploma Common Entrance Test\\[0.3em]\large Question Paper with Solutions}
\author{}
\date{}

\begin{document}

\maketitle
\thispagestyle{empty}

\vspace{1cm}

\section*{Instructions}
\begin{itemize}
    \item Total Questions: 100
    \item Maximum Marks: 100
    \item Each question carries 1 mark
    \item Duration: 3 hours
\end{itemize}

\newpage

'''

# Read CSV and organize by sections
sections = {}
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        section = row['section_name'].strip()
        if not section:
            continue
        if section not in sections:
            sections[section] = []
        sections[section].append(row)

# Generate questions by section
for section_name, questions in sections.items():
    if not section_name:
        continue
    
    # Add section heading
    latex_content += f"\\section*{{{section_name}}}\n\n"
    latex_content += "\\begin{enumerate}[resume]\n\n"
    
    for q in questions:
        q_num = q['question_number']
        q_text = q['question_text'].strip()
        opt_a = q['option_a'].strip()
        opt_b = q['option_b'].strip()
        opt_c = q['option_c'].strip()
        opt_d = q['option_d'].strip()
        correct = q['correct_option'].strip()
        
        # Add question
        latex_content += f"\\item {q_text}\n\n"
        latex_content += "\\begin{enumerate}[label=(\\Alph*)]\n"
        latex_content += f"    \\item {opt_a}\n"
        latex_content += f"    \\item {opt_b}\n"
        latex_content += f"    \\item {opt_c}\n"
        latex_content += f"    \\item {opt_d}\n"
        latex_content += "\\end{enumerate}\n\n"
        latex_content += f"\\textbf{{Answer: ({correct})}}\\\\[0.5em]\n\n"
    
    latex_content += "\\end{enumerate}\n\n"
    latex_content += "\\newpage\n\n"

# End document
latex_content += "\\end{document}"

# Write LaTeX file
with open('dcet_2023_question_paper.tex', 'w', encoding='utf-8') as f:
    f.write(latex_content)

print("✓ LaTeX file created: dcet_2023_question_paper.tex")
print("\nTo generate PDF, run:")
print("  pdflatex dcet_2023_question_paper.tex")
print("\nOr use an online LaTeX compiler like Overleaf.")
