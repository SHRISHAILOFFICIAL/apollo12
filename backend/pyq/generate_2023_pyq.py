"""
Generate DCET 2023 PYQ HTML — questions only, print-optimized, with MathJax.
Open in Chrome → Ctrl+P → Save as PDF for perfect output.
"""
import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'dcet_pyq_2023.csv')
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), 'DCET_2023_PYQ_Questions.html')

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

# Section accent colors
COLORS = [
    '#4f46e5',  # Indigo - IT Skills
    '#0891b2',  # Cyan - EEE
    '#059669',  # Green - Project Mgmt
    '#d97706',  # Amber - Eng Maths
    '#dc2626',  # Red - Statistics
    '#7c3aed',  # Purple - extra
]

html = []

# ─── HEAD ────────────────────────────────────────────────────
html.append(r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DCET 2023 — Previous Year Questions</title>
<script>
MathJax = {
  tex: { inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']] },
  options: { skipHtmlTags: ['script','noscript','style','textarea'] }
};
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
/* ── RESET & BASE ── */
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
  font-size:11px;line-height:1.5;color:#1e293b;
  background:#f1f5f9;
}

/* ── PRINT ── */
@page{size:A4;margin:12mm 14mm}
@media print{
  body{background:#fff;font-size:10px}
  .no-print{display:none!important}
  .paper{box-shadow:none;margin:0;padding:0;border:none;max-width:none}
  .q-item{break-inside:avoid}
  .sec-hdr{break-after:avoid}
}

/* ── PAPER ── */
.paper{
  max-width:210mm;margin:16px auto;background:#fff;
  padding:24px 28px;
}

/* ── HEADER ── */
.hdr{text-align:center;padding-bottom:14px;margin-bottom:14px;
     border-bottom:2.5px solid #4f46e5;position:relative}
.hdr::after{content:'';position:absolute;bottom:-2.5px;left:25%;
            width:50%;height:2.5px;background:linear-gradient(90deg,#a855f7,#4f46e5)}
.hdr h1{font-size:28px;font-weight:800;color:#1e1b4b;letter-spacing:1.5px}
.hdr .sub{font-size:13px;color:#64748b;margin-top:2px;font-weight:500}
.badge{display:inline-block;margin-top:8px;
       background:linear-gradient(135deg,#4f46e5,#7c3aed);
       color:#fff;padding:3px 18px;border-radius:20px;
       font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase}

/* ── INFO BAR ── */
.info{display:flex;justify-content:center;gap:18px;flex-wrap:wrap;
      padding:6px 0 10px;margin-bottom:10px;font-size:10px;color:#475569;
      border-bottom:1px dashed #e2e8f0}
.info b{color:#312e81}

/* ── SECTION HEADER ── */
.sec-hdr{
  color:#fff;padding:6px 14px;font-size:11px;font-weight:700;
  letter-spacing:1px;text-transform:uppercase;margin:14px 0 8px;
  border-radius:3px;
}

/* ── QUESTION LIST ── */
.q-list{padding:0;list-style:none}

.q-item{
  display:flex;gap:8px;align-items:flex-start;
  padding:6px 0;
  border-bottom:1px solid #f1f5f9;
}
.q-item:last-child{border-bottom:none}

.q-num{
  flex-shrink:0;width:32px;
  font-weight:800;font-size:11px;
  padding-top:1px;
}

.q-body{flex:1;min-width:0}
.q-text{font-size:11px;color:#1e293b;margin-bottom:4px;line-height:1.55}

/* ── OPTIONS GRID ── */
.opts{
  display:grid;grid-template-columns:1fr 1fr;
  gap:2px 12px;margin-left:2px;
}
.opt{font-size:10.5px;color:#334155;padding:1px 0;line-height:1.45;display:flex;gap:4px}
.opt-lbl{font-weight:700;flex-shrink:0}

/* ── FOOTER ── */
.ftr{text-align:center;margin-top:18px;padding-top:8px;
     border-top:2px solid #4f46e5;font-size:9px;color:#94a3b8}

/* ── PRINT BUTTON ── */
.no-print{
  position:fixed;top:16px;right:16px;z-index:999;
  background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;border:none;
  padding:10px 24px;border-radius:24px;font-size:13px;font-weight:700;
  cursor:pointer;box-shadow:0 4px 16px rgba(79,70,229,.35);
  letter-spacing:.3px;
}
.no-print:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(79,70,229,.45)}
</style>
</head>
<body>
<button class="no-print" onclick="window.print()">&#128424; Save as PDF</button>
<div class="paper">

<div class="hdr">
  <h1>DCET 2023</h1>
  <div class="sub">Diploma Common Entrance Test &mdash; Previous Year Questions</div>
  <div class="badge">Questions Only &bull; Practice Paper</div>
</div>

<div class="info">
  Total Questions: <b>&nbsp;100&nbsp;</b> &vert;
  Maximum Marks: <b>&nbsp;100&nbsp;</b> &vert;
  Duration: <b>&nbsp;3 Hours&nbsp;</b> &vert;
  Each Question: <b>&nbsp;1 Mark</b>
</div>
''')

# ─── SECTIONS & QUESTIONS ────────────────────────────────────
for idx, (sec_name, sec_qs) in enumerate(sections.items()):
    color = COLORS[idx % len(COLORS)]
    html.append(f'<div class="sec-hdr" style="background:{color}">{sec_name}</div>\n')
    html.append('<ol class="q-list">\n')

    for q in sec_qs:
        qnum = q['question_number']
        # Use question_text (has LaTeX) for math sections, plain_text otherwise
        qtext = q['question_text'].strip()
        opts = [q.get('option_a',''), q.get('option_b',''), q.get('option_c',''), q.get('option_d','')]

        html.append(f'<li class="q-item">\n')
        html.append(f'  <div class="q-num" style="color:{color}">Q{qnum}.</div>\n')
        html.append(f'  <div class="q-body">\n')
        html.append(f'    <div class="q-text">{qtext}</div>\n')
        html.append(f'    <div class="opts">\n')
        for i, opt in enumerate(opts):
            label = chr(65 + i)
            html.append(f'      <div class="opt"><span class="opt-lbl" style="color:{color}">({label})</span> <span>{opt}</span></div>\n')
        html.append(f'    </div>\n')
        html.append(f'  </div>\n')
        html.append(f'</li>\n')

    html.append('</ol>\n')

# ─── FOOTER ──────────────────────────────────────────────────
html.append('''
<div class="ftr">
  DCET 2023 &mdash; Previous Year Questions &bull; For Practice Purpose Only &bull; apollo12
</div>
</div>
</body>
</html>
''')

# Write output
with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(''.join(html))

print(f"Generated: {OUTPUT_HTML}")
print(f"Total questions: {len(questions)}")
print(f"Sections: {len(sections)}")
print("→  Open in Chrome → Ctrl+P → Save as PDF")
