import sys
import sqlite3
from pathlib import Path

# Add project root (interview-coach) to PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai.scorer import score_answer
from ai.nlp_processor import get_embedding

DB_PATH = Path(__file__).resolve().parents[1] / 'database.db'
print('DB path:', DB_PATH)
print('DB exists?', DB_PATH.exists())

question_id = 110
test_answer = (
    "Denormalization duplicates data to avoid joins, improving read performance "
    "but risking consistency issues. It’s a trade‑off between speed and storage."
)

# Fetch question text
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
cur.execute('SELECT question_text FROM Questions WHERE id = ?', (question_id,))
row = cur.fetchone()
question_text = row[0] if row else '<NOT FOUND>'
print('Question text:', question_text)

# Fetch excellent reference answer
cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id = ? AND label = 'Excellent'", (question_id,))
ref_row = cur.fetchone()
ref_answer = ref_row[0] if ref_row else '<NO EXCELLENT>'
print('Excellent reference answer (first 200 chars):', ref_answer[:200])

# Score
label, sim = score_answer(question_id, test_answer)
print('Score label:', label)
print('Raw similarity (full):', sim)

# Embedding lengths
ref_emb = get_embedding(ref_answer)
test_emb = get_embedding(test_answer)
print('Embedding length (reference):', len(ref_emb))
print('Embedding length (test):', len(test_emb))

# Raw cosine
import numpy as np

def cosine(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

raw_cos = cosine(test_emb, ref_emb)
print('Raw cosine similarity (unrounded):', raw_cos)

conn.close()
