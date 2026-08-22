import os, sys, sqlite3
# Ensure project root is on PYTHONPATH for 'ai' package imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from ai.feedback_engine import get_missing_concepts

# Determine DB path (project root)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(base_dir, 'database.db')
if not os.path.exists(db_path):
    db_path = 'database.db'

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Get four distinct question IDs with Excellent answers
cur.execute("SELECT DISTINCT question_id FROM ReferenceAnswers WHERE label='Excellent' LIMIT 4")
question_ids = [row[0] for row in cur.fetchall()]

print('Testing get_missing_concepts on 4 questions')
for qid in question_ids:
    # Fetch Excellent reference answer (use as strong answer)
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id=? AND label='Excellent'", (qid,))
    ref_row = cur.fetchone()
    if not ref_row:
        continue
    strong_answer = ref_row[0]
    missing = get_missing_concepts(qid, strong_answer, db_path=db_path)
    # Fetch question text
    cur.execute("SELECT question_text FROM Questions WHERE question_id=?", (qid,))
    q_text = cur.fetchone()[0]
    print('\n---')
    print(f'Question ID: {qid}')
    print('Question:', q_text)
    print('Strong Answer Used:', strong_answer)
    print('Missing Concepts:', missing)

conn.close()
