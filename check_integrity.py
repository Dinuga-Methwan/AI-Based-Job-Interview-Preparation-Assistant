import os, sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check duplicate question_text
cur.execute('''
SELECT question_text, COUNT(*) as cnt
FROM Questions
GROUP BY question_text
HAVING cnt > 1
''')
duplicates = cur.fetchall()
if duplicates:
    print('Duplicate question_text entries found:')
    for txt, cnt in duplicates:
        print(f'Count {cnt}: {repr(txt)[:80]}...')
else:
    print('No duplicate question_text entries.')

# Check ReferenceAnswers count per question_id
cur.execute('''
SELECT question_id, COUNT(*) as cnt
FROM ReferenceAnswers
GROUP BY question_id
HAVING cnt != 4
''')
odd_counts = cur.fetchall()
if odd_counts:
    print('\nReferenceAnswers count issues (question_id, count):')
    for qid, cnt in odd_counts:
        print(f'Question ID {qid}: {cnt} answers')
else:
    print('\nAll questions have exactly 4 reference answers.')

conn.close()
