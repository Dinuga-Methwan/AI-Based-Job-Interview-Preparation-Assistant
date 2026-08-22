import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT id, question_text FROM Questions WHERE question_type = 'Behavioral'")
rows = cur.fetchall()
for r in rows:
    print(f"{r[0]}: {r[1]}")
conn.close()
