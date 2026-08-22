import os, csv, re

DATA_DIR = 'data'
CSV_FILES = [
    os.path.join(DATA_DIR, 'software_engineer_labeled_dataset.csv'),
    os.path.join(DATA_DIR, 'behavioral_labeled_dataset.csv')
]

# Regex for invisible Unicode characters
invisible_pattern = re.compile(r'[\u200b\u200c\u200d\ufeff]')

for csv_path in CSV_FILES:
    if not os.path.exists(csv_path):
        print(f'File not found: {csv_path}')
        continue
    print(f'Scanning {csv_path}')
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # start=2 to account for header line
            for col, val in row.items():
                if val and invisible_pattern.search(val):
                    print(f'Row {i}, Column "{col}": contains invisible character')
print('Scan complete')
