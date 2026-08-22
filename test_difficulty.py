import os, sqlite3
from ai.feedback_engine import get_next_difficulty

DB_PATH = os.path.abspath('database.db')
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Create a fresh session (will use default difficulty Medium)
c.execute("INSERT INTO Sessions (job_role) VALUES (?);", ('Software Engineer',))
conn.commit()
session_id = c.lastrowid
print('Created session id:', session_id)

# Simulated score sequence
scores = ['Excellent', 'Excellent', 'Poor', 'Average', 'Excellent']

for i, score in enumerate(scores, 1):
    cur = c.execute("SELECT current_difficulty FROM Sessions WHERE id = ?;", (session_id,)).fetchone()['current_difficulty']
    new = get_next_difficulty(cur, score)
    c.execute("UPDATE Sessions SET current_difficulty = ? WHERE id = ?;", (new, session_id))
    conn.commit()
    print(f"Step {i}: score={score:9s} | before={cur:6s} -> after={new}")

conn.close()
