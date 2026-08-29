import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Check if column already exists before adding, to make this safe to re-run
cur.execute("PRAGMA table_info(Sessions)")
columns = [row[1] for row in cur.fetchall()]

if 'user_id' not in columns:
    cur.execute("ALTER TABLE Sessions ADD COLUMN user_id INTEGER REFERENCES Users(id)")
    conn.commit()
    print("Added user_id column to Sessions table.")
else:
    print("user_id column already exists, no changes made.")

conn.close()
