import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Show all rows where question_type contains 'Behavioral'
cur.execute("SELECT id, question_type, question_text FROM Questions WHERE question_type LIKE '%Behavioral%'")
rows = cur.fetchall()
print('Rows with question_type LIKE "%Behavioral%":')
for r in rows:
    qid, qtype, qtext = r
    print(f'ID:{qid} type:{repr(qtype)} len:{len(qtype)} text:{qtext[:60]}...')
conn.close()
