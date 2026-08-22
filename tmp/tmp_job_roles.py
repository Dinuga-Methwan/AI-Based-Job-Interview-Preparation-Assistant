import sqlite3, os

db_path = os.path.join(os.getcwd(), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('SELECT job_role, COUNT(*) FROM Questions GROUP BY job_role')
rows = cur.fetchall()
print('Job role counts:')
for role, cnt in rows:
    print(f'  {role!r}: {cnt}')

cur.execute('SELECT DISTINCT job_role FROM Questions')
roles = cur.fetchall()
print('Distinct roles:', roles)

conn.close()
