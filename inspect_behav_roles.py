import os, csv, collections

data_dir = 'data'
behav_path = os.path.join(data_dir, 'behavioral_labeled_dataset.csv')
roles = set()
with open(behav_path, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        roles.add(row['Job Role'])
print('Distinct Job Role values in behavioral CSV:')
for r in roles:
    print(repr(r))
