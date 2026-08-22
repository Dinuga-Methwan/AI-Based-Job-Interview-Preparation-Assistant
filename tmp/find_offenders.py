import os, sys, sqlite3, json
sys.path.insert(0, os.getcwd())
from ai.nlp_processor import extract_keywords, clean_text

db_path = os.path.join(os.getcwd(), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('SELECT id, answer_text FROM ReferenceAnswers')
rows = cur.fetchall()
offenders = []
for aid, txt in rows:
    kws = extract_keywords(txt)
    if 'expense' in kws or 'readheavy' in kws:
        offenders.append((aid, txt, kws))
print('offenders count:', len(offenders))
for aid, txt, kws in offenders:
    print('---')
    print('ID:', aid)
    print('Answer text:', txt)
    print('Keywords:', kws)
conn.close()
