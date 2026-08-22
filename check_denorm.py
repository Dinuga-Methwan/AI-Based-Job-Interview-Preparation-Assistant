import sqlite3
c = sqlite3.connect('database.db')
rows = c.execute("SELECT id, question_text FROM Questions WHERE question_text LIKE '%denormal%'").fetchall()
print(rows)