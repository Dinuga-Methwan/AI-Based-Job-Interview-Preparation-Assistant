import os, sys, sqlite3
# Add project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from ai.feedback_engine import get_missing_concepts

# DB path
db_path = os.path.join(project_root, 'database.db')
if not os.path.exists(db_path):
    db_path = 'database.db'

conn = sqlite3.connect(db_path)
cur = conn.cursor()

weak_answers = {
    23: "It's used to organize data.",
    57: "It helps keep things consistent.",
    89: "It makes queries faster."
}

print('Testing get_missing_concepts with weak/vague answers')
for qid, ans in weak_answers.items():
    cur.execute("SELECT question_text FROM Questions WHERE question_id=?", (qid,))
    q_text = cur.fetchone()[0]
    missing = get_missing_concepts(qid, ans, db_path=db_path)
    print('\n---')
    print(f'Question ID: {qid}')
    print('Question:', q_text)
    print('Weak Answer Used:', ans)
    print('Missing Concepts:', missing)

conn.close()
