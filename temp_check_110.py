import sqlite3, json
c = sqlite3.connect('database.db')
q = c.execute('SELECT id, question_text FROM Questions WHERE id=110').fetchall()
ra = c.execute('SELECT label, answer_text FROM ReferenceAnswers WHERE question_id=110').fetchall()
print('Question row:', json.dumps(q, ensure_ascii=False))
print('Reference answers:', json.dumps(ra, ensure_ascii=False))
