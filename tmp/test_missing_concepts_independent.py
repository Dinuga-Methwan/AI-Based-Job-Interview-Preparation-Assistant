import os, sys, sqlite3
# Ensure project root is on PYTHONPATH for 'ai' imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from ai.feedback_engine import get_missing_concepts

# Database path
db_path = os.path.join(project_root, 'database.db')
if not os.path.exists(db_path):
    db_path = 'database.db'

conn = sqlite3.connect(db_path)
cur = conn.cursor()

answers = {
    23: "A primary key makes sure every row in a table is unique and can be identified on its own. A foreign key sits in one table but points back to the primary key in a different table, which is how the two tables get linked together.",
    57: "In distributed systems, eventual consistency means the different copies of data won't always match up immediately after a change. If you read right after an update, you might get an old value. But as long as nothing else changes, every copy will eventually catch up and match.",
    89: "When a query is running slowly, I'd start by checking the query plan to see where time is being spent. Usually adding an index on the right column helps a lot. I'd also look at whether any subqueries could be rewritten as joins, and make sure I'm not filtering on a huge unindexed column.",
    110: "Denormalizing a database means keeping some duplicate data around so you don't have to do as many joins, which makes reads faster. The downside is you now have to keep that duplicate data in sync, which adds complexity and risk of inconsistency."
}

print('Testing get_missing_concepts with independently worded strong answers')
for qid, ans in answers.items():
    cur.execute("SELECT question_text FROM Questions WHERE question_id=?", (qid,))
    q_text = cur.fetchone()[0]
    missing = get_missing_concepts(qid, ans, db_path=db_path)
    print('\n---')
    print(f'Question ID: {qid}')
    print('Question:', q_text)
    print('Answer Used:', ans)
    print('Missing Concepts:', missing)

conn.close()
