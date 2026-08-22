import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('SELECT DISTINCT job_role FROM Questions')
roles = cur.fetchall()
print('Distinct job_role values in DB:')
for r in roles:
    print(repr(r[0]), f'len={len(r[0])}')
conn.close()
