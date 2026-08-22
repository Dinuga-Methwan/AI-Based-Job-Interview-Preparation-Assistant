import os, sqlite3
from ai.scorer import score_answer

# DB path same as app
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
question = "How do you contribute to a positive team environment?"
cur.execute("SELECT id FROM Questions WHERE question_text LIKE ?", (f'%{question}%',))
row = cur.fetchone()
if not row:
    print('Question not found')
else:
    qid = row[0]
    answer = """I contribute to a positive team environment by communicating clearly, respecting everyone's ideas, and being willing to help my team members. I make sure to complete my assigned tasks on time and keep the team updated about my progress. If a teammate has a problem, I try to support them and find a solution together. I also accept feedback positively and stay open to learning from others."""
    label, sim = score_answer(qid, answer)
    print(f'Similarity: {sim}, Label: {label}')

