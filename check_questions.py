import sqlite3, pathlib

db_path = pathlib.Path('database.db')
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()
cur.execute('SELECT id, question_text FROM Questions LIMIT 20')
rows = cur.fetchall()
print('First 20 questions:')
for r in rows:
    print(r[0], r[1][:80])
cur.execute('SELECT COUNT(*) FROM Questions')
print('Total questions:', cur.fetchone()[0])
conn.close()