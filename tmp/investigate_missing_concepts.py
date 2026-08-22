import os, sys, sqlite3
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from ai.nlp_processor import extract_keywords, clean_text

# DB path
db_path = project_root / 'database.db'
if not db_path.exists():
    db_path = Path('database.db')

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()
cur.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE ?", ("%denormal%",))
row = cur.fetchone()
print('Question row (id, text):', row)
if row:
    q_id = row[0]
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id=? AND label='Excellent'", (q_id,))
    ref = cur.fetchone()
    ref_text = ref[0] if ref else None
    print('Excellent reference answer (repr):', repr(ref_text))
    if ref_text:
        keywords = extract_keywords(ref_text)
        print('Extracted keywords (repr):', repr(keywords))
else:
    print('No denormalization question found')
conn.close()
