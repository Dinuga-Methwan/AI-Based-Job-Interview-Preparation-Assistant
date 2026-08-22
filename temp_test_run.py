import sqlite3, pathlib, sys
from ai.scorer import score_answer
from ai.feedback_engine import get_missing_concepts

# get a question id for denormal
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("SELECT id FROM Questions WHERE question_text LIKE ?", ('%denormal%',))
row = cur.fetchone()
print('question row', row)
if row:
    qid = row[0]
    label, _ = score_answer(qid, "Denormalization duplicates data ...")
    print('score label', label)
    missing = get_missing_concepts(qid, "Denormalization duplicates data ...")
    print('missing', missing)
else:
    print('no question found')
