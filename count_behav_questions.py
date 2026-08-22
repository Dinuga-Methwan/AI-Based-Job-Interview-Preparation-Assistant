import os, csv, collections

data_dir='data'
behav_path=os.path.join(data_dir,'behavioral_labeled_dataset.csv')
questions=set()
with open(behav_path, newline='', encoding='utf-8-sig') as f:
    reader=csv.DictReader(f)
    for row in reader:
        q=row['Question']
        questions.add(q)
print('Distinct question texts in behavioral CSV:', len(questions))
