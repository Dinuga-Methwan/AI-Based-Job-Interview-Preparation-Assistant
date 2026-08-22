import os, sqlite3
from ai.scorer import score_answer

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
question_text = "What skills do you hope to develop in the next role?"
cur.execute("SELECT id FROM Questions WHERE question_text = ?", (question_text,))
qid_row = cur.fetchone()
if not qid_row:
    print('Question not found')
else:
    qid = qid_row[0]
    user_answer = "In my next role, I hope to further develop both my technical and professional skills. I would like to improve my knowledge of industry tools and technologies, gain more hands‑on experience, and strengthen my problem‑solving abilities. I also want to develop my communication, teamwork, and leadership skills by working with experienced professionals and contributing to real projects. I believe continuous learning is important for both personal growth and career success."
    label, sim = score_answer(qid, user_answer, db_path=db_path)
    print('Similarity score:', sim)
    print('Predicted label:', label)
conn.close()
