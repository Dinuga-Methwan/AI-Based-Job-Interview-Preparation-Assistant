import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('SELECT job_role, COUNT(*) FROM Questions GROUP BY job_role')
rows = cur.fetchall()
print('Job role counts:')
for role, cnt in rows:
    print(f"{repr(role)} (len={len(role)}): {cnt}")
conn.close()
