import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
question_text = "What skills do you hope to develop in your next role?"
cur.execute("SELECT id FROM Questions WHERE question_text = ?", (question_text,))
row = cur.fetchone()
if row:
    qid = row[0]
    print('Question ID:', qid)
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id = ? AND label = 'Excellent'", (qid,))
    ans = cur.fetchone()
    if ans:
        print('Stored Excellent reference answer:')
        print(ans[0])
    else:
        print('No Excellent reference answer found')
else:
    print('Question not found')
conn.close()
