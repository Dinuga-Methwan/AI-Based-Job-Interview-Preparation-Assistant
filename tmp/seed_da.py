import csv
import sqlite3
import re
import os

DB_PATH = 'database.db' # since in same root
csv_path = os.path.join('data', 'data_analyst_questions.csv')

def clean_text(value: str) -> str:
    """Strip invisible Unicode characters and surrounding whitespace."""
    if not isinstance(value, str):
        return value
    cleaned = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', value)
    return cleaned.strip()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

inserted = 0

with open(csv_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        q_text = clean_text(row['Question'])
        job_role = clean_text(row['Job Role'])
        q_type = clean_text(row['Question Type'])
        category = clean_text(row['Category'])
        difficulty = clean_text(row.get('Difficulty', 'Medium'))
        ans_text = clean_text(row['Answer'])
        label = clean_text(row['Label'])

        # Check if question exists first to avoid unnecessary inserts if rerunning
        cursor.execute("SELECT id FROM Questions WHERE question_text = ?", (q_text,))
        res = cursor.fetchone()
        if res:
            q_id = res[0]
            # check if reference answer already exists
            cursor.execute("SELECT id FROM ReferenceAnswers WHERE question_id=? AND label=?", (q_id, label))
            if cursor.fetchone():
                continue # Skip if already inserted
        else:
            # insert new question
            cursor.execute(
                "INSERT INTO Questions (job_role, question_type, category, difficulty, question_text) VALUES (?, ?, ?, ?, ?)",
                (job_role, q_type, category, difficulty, q_text)
            )
            q_id = cursor.lastrowid
            
        cursor.execute(
            "INSERT INTO ReferenceAnswers (question_id, answer_text, label) VALUES (?, ?, ?)",
            (q_id, ans_text, label)
        )
        inserted += 1

conn.commit()

cursor.execute("SELECT COUNT(*) FROM Questions WHERE job_role='Data Analyst';")
q_count = cursor.fetchone()[0]

conn.close()
print(f"Added {inserted} answer records.")
print(f"Total Unique Data Analyst questions in DB: {q_count}")
