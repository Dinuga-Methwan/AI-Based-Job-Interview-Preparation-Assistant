import os, sys, json, sqlite3
# Ensure project root is on sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from ai.nlp_processor import extract_keywords, clean_text
# Database path
db_path = os.path.join(project_root, 'database.db')
if not os.path.exists(db_path):
    db_path = 'database.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Find question id containing 'denormal'
cur.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE ?", ("%denormal%",))
row = cur.fetchone()
print('question_row:', json.dumps(row))
if row:
    q_id = row[0]
    # Fetch Excellent reference answer
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id=? AND label='Excellent'", (q_id,))
    ref = cur.fetchone()
    ref_text = ref[0] if ref else None
    print('reference_answer:', json.dumps(ref_text))
    if ref_text:
        keywords = extract_keywords(ref_text)
        print('extracted_keywords:', json.dumps(keywords))
conn.close()
