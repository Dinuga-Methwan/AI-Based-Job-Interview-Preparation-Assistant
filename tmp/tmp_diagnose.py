import sqlite3, os
db_path = os.path.join(os.getcwd(), 'database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT id, question_text, job_role FROM Questions WHERE question_text LIKE '%denormal%'")
rows = cur.fetchall()
print("Denormalization questions found:", rows)

if rows:
    qids = [r[0] for r in rows]
    placeholders = ",".join("?" * len(qids))
    cur.execute(f"SELECT question_id, label, answer_text FROM ReferenceAnswers WHERE question_id IN ({placeholders})", qids)
    print("Reference answers for those IDs:")
    for r in cur.fetchall():
        print(" -", r[0], r[1], ":", r[2][:150])

cur.execute("SELECT DISTINCT job_role FROM Questions")
print("All distinct job_role values:", cur.fetchall())

cur.execute("SELECT job_role, COUNT(*) FROM Questions GROUP BY job_role")
print("Job role counts:", cur.fetchall())

conn.close()
