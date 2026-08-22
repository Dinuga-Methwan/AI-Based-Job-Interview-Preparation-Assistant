import os, sys, sqlite3, json, pathlib

# Determine project root (interview-coach directory)
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from ai.nlp_processor import extract_keywords, clean_text

# Locate the SQLite database
db_path = project_root / 'database.db'
if not db_path.exists():
    db_path = pathlib.Path('database.db')

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()
# Find the question containing 'denormal' in its text
cur.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE ?", ("%denormal%",))
row = cur.fetchone()
print('question_row:', json.dumps(row))
if row:
    qid = row[0]
    # Fetch the Excellent reference answer for this question
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id=? AND label='Excellent'", (qid,))
    ref = cur.fetchone()
    print('reference_answer:', json.dumps(ref[0] if ref else None))
    if ref:
        # Extract keywords from the reference answer
        kw = extract_keywords(ref[0])
        print('keywords:', json.dumps(kw))
conn.close()
