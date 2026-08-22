import os
import csv
import sqlite3
import re

DB_PATH = 'database.db'
DATA_DIR = 'data'
DATASETS = [
    os.path.join(DATA_DIR, 'software_engineer_labeled_dataset.csv'),
    os.path.join(DATA_DIR, 'behavioral_labeled_dataset.csv')
]

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_role TEXT NOT NULL,
            question_type TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question_text TEXT NOT NULL UNIQUE
        );
    """)
    # ReferenceAnswers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ReferenceAnswers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            label TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES Questions (id) ON DELETE CASCADE
        );
    """)
    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_role TEXT NOT NULL,
            current_difficulty TEXT NOT NULL DEFAULT 'Medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # UserAnswers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserAnswers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            score_label TEXT,
            feedback_text TEXT,
            FOREIGN KEY (session_id) REFERENCES Sessions (id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES Questions (id) ON DELETE CASCADE
        );
    """)
    conn.commit()

def clean_text(value: str) -> str:
    """Strip invisible Unicode characters and surrounding whitespace."""
    if not isinstance(value, str):
        return value
    cleaned = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', value)
    return cleaned.strip()

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    cursor = conn.cursor()
    # Clear existing data
    cursor.execute("DELETE FROM ReferenceAnswers;")
    cursor.execute("DELETE FROM Questions;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('Questions', 'ReferenceAnswers');")
    conn.commit()
    # Insert each row directly, preserving job_role per CSV row
    for dataset_path in DATASETS:
        if not os.path.exists(dataset_path):
            print(f"Warning: File {dataset_path} not found.")
            continue
        with open(dataset_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_text = clean_text(row['Question'])
                job_role = clean_text(row['Job Role'])
                q_type = clean_text(row['Question Type'])
                category = clean_text(row['Category'])
                difficulty = clean_text(row.get('Difficulty', 'Medium'))
                ans_text = clean_text(row['Answer'])
                label = clean_text(row['Label'])
                # Insert question (ignore duplicate question_text errors)
                try:
                    cursor.execute(
                        "INSERT INTO Questions (job_role, question_type, category, difficulty, question_text) VALUES (?, ?, ?, ?, ?)",
                        (job_role, q_type, category, difficulty, q_text)
                    )
                    question_id = cursor.lastrowid
                except sqlite3.IntegrityError:
                    # Question already exists (same text). Retrieve its id.
                    cursor.execute("SELECT id FROM Questions WHERE question_text = ?", (q_text,))
                    question_id = cursor.fetchone()[0]
                # Insert reference answer
                cursor.execute(
                    "INSERT INTO ReferenceAnswers (question_id, answer_text, label) VALUES (?, ?, ?)",
                    (question_id, ans_text, label)
                )
    conn.commit()
    # Summary counts
    cursor.execute("SELECT COUNT(*) FROM Questions;")
    q_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ReferenceAnswers;")
    a_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Sessions;")
    s_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM UserAnswers;")
    ua_cnt = cursor.fetchone()[0]
    conn.close()
    print("--- Database Seeding Completed ---")
    print(f"Questions table count: {q_cnt}")
    print(f"ReferenceAnswers table count: {a_cnt}")
    print(f"Sessions table count: {s_cnt}")
    print(f"UserAnswers table count: {ua_cnt}")

if __name__ == '__main__':
    seed_database()
