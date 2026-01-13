"""
Script to convert DCET 2025 CSV from full math mode ($...$) to selective LaTeX style
This will make it consistent with DCET 2023 formatting
"""
import csv
import re

def convert_latex_style(text):
    """
    Convert from: $\text{question text with } \math{symbols}$
    To: question text with \(math symbols\)
    """
    if not text or text.strip() == '':
        return text
    
    # Remove outer $ delimiters if present
    text = text.strip()
    if text.startswith('$') and text.endswith('$'):
        text = text[1:-1]  # Remove outer $...$
    
    # Convert inner math expressions
    # Keep \text{} content as plain text
    # Wrap standalone math in \(...\)
    
    # For now, just remove the outer $ and keep everything else
    # The frontend should handle \text{} and math symbols
    
    return text

# Read the 2025 CSV
input_file = 'dcet_pyq_2025.csv'
output_file = 'dcet_pyq_2025_converted.csv'

with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    
    rows = []
    for row in reader:
        # Convert question_text
        row['question_text'] = convert_latex_style(row['question_text'])
        
        # Convert options (they might also have $...$)
        for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
            row[opt] = convert_latex_style(row[opt])
        
        rows.append(row)

# Write converted CSV
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Converted {len(rows)} questions")
print(f"📝 Output saved to: {output_file}")
print("\nNext steps:")
print("1. Review the converted file")
print("2. Replace dcet_pyq_2025.csv with the converted version")
print("3. Test the rendering in the application")
