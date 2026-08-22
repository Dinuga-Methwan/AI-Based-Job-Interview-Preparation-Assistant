import sys
from pathlib import Path
import sqlite3

# Add project root (interview-coach) to PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai.scorer import score_answer
from ai.nlp_processor import get_embedding

DB_PATH = Path(__file__).resolve().parents[1] / 'database.db'
print('DB path:', DB_PATH)
print('DB exists?', DB_PATH.exists())

def fetch_question_text(qid: int) -> str:
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute('SELECT question_text FROM Questions WHERE id = ?', (qid,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else '<NOT FOUND>'

def fetch_excellent_answer(qid: int) -> str:
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id = ? AND label = 'Excellent'", (qid,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else '<NO EXCELLENT>'

question_id = 110
test_answer = (
    "Denormalization duplicates data to avoid joins, improving read performance "
    "but risking consistency issues. It’s a trade‑off between speed and storage."
)

# 1. Question text
qt = fetch_question_text(question_id)
print('Question text:', qt)

# 2. Excellent reference answer
ref_ans = fetch_excellent_answer(question_id)
print('Excellent reference answer (first 200 chars):', ref_ans[:200])

# 3. Score and raw similarity
label, sim = score_answer(question_id, test_answer)
print('Score label:', label)
print('Raw similarity (rounded to 4dp):', round(sim, 4))

# 4. Embedding lengths and raw cosine similarity
ref_emb = get_embedding(ref_ans)
test_emb = get_embedding(test_answer)
print('Embedding length (reference):', len(ref_emb))
print('Embedding length (test answer):', len(test_emb))

import numpy as np

def cosine(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

raw_cos = cosine(test_emb, ref_emb)
print('Raw cosine similarity (unrounded):', raw_cos)
