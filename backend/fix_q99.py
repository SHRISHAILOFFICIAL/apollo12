import csv

# Read CSV
with open('dcet_pyq_2023.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

# Find and update Q99
for row in rows:
    if row['question_number'] == '99':
        row['option_a'] = "(' ')"
        row['option_b'] = '(" ")'
        row['option_c'] = '( )'
        row['option_d'] = '(""" """)'
        print(f"Updated Q99:")
        print(f"  A: {row['option_a']}")
        print(f"  B: {row['option_b']}")
        print(f"  C: {row['option_c']}")
        print(f"  D: {row['option_d']}")
        break

# Write back
with open('dcet_pyq_2023.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("✅ Q99 fixed in CSV")
