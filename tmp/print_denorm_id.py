import os, sqlite3, sys
# Determine project root (one level up from this script's directory)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(base_dir, 'database.db')
if not os.path.exists(db_path):
    db_path = 'database.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Lookup question id by text containing 'denormal'
cur.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE ?", ("%denormal%",))
rows = cur.fetchall()
print('Question rows:', rows)
if rows:
    q_id = rows[0][0]
    # Get Excellent reference answer
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id = ? AND label = 'Excellent'", (q_id,))
    ref = cur.fetchone()
    print('Reference answer:', ref[0] if ref else None)
else:
    print('No denormal question found')
conn.close()
