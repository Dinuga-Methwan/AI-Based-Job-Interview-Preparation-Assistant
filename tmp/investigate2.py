import os, sys, sqlite3
# Add project root to path
project_root = os.path.abspath(os.getcwd())
sys.path.insert(0, project_root)
from ai.nlp_processor import extract_keywords, clean_text
# DB path
db_path = os.path.join(project_root, 'database.db')
if not os.path.exists(db_path):
    db_path = 'database.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Find question id containing 'denormal'
cur.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE ?", ("%denormal%",))
row = cur.fetchone()
print('Question row:', row)
if row:
    q_id = row[0]
    # Get Excellent reference answer
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id=? AND label='Excellent'", (q_id,))
    ref = cur.fetchone()
    print('Reference answer:', ref[0] if ref else None)
    if ref:
        kw = extract_keywords(ref[0])
        print('Extracted keywords:', kw)
else:
    print('No denormal question found')
conn.close()
