import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# distinct question_type
cur.execute('SELECT DISTINCT question_type FROM Questions')
qt = [row[0] for row in cur.fetchall()]
# distinct job_role
cur.execute('SELECT DISTINCT job_role FROM Questions')
jr = [row[0] for row in cur.fetchall()]
print('Question Types:')
for t in qt:
    print(f' - {t}')
print('Job Roles:')
for r in jr:
    print(f' - {r}')
conn.close()
