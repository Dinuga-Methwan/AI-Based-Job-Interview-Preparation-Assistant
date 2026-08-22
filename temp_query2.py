import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE ? AND question_text LIKE ?", ('%team%','%environment%'))
rows = cur.fetchall()
for row in rows:
    print(f"{row[0]}: {row[1]}")
conn.close()
