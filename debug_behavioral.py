import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Fetch distinct question_type values and show repr
cur.execute('SELECT DISTINCT question_type FROM Questions')
types = cur.fetchall()
print('Distinct question_type values (repr):')
for t in types:
    print(repr(t[0]))
# Verify rows with exact 'Behavioral'
cur.execute("SELECT id, question_text FROM Questions WHERE question_type = 'Behavioral' AND question_text LIKE ? AND question_text LIKE ?", ('%team%','%environment%'))
rows = cur.fetchall()
print('\nRows matching Behavioral & team & environment:')
for r in rows:
    print(f'{r[0]}: {r[1]}')
conn.close()
