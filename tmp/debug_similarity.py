import sys
import sqlite3
from pathlib import Path
# Add project root (interview-coach) to PYTHONPATH so that the 'ai' package can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai.scorer import score_answer
from ai.nlp_processor import get_embedding

def _db_path() -> str:
    base_dir = Path(__file__).resolve().parents[1]
    db_path = base_dir / "database.db"
    if not db_path.exists():
        db_path = Path("database.db")
    return str(db_path)

# 1. Question text for ID 110
conn = sqlite3.connect(_db_path())
cur = conn.cursor()
cur.execute("SELECT question_text FROM Questions WHERE id = ?", (110,))
row = cur.fetchone()
question_text = row[0] if row else "<NOT FOUND>"
print("Question text:", question_text)

# 2. Excellent reference answer for ID 110
cur.execute("SELECT answer_text FROM ReferenceAnswers WHERE question_id = ? AND label = 'Excellent'", (110,))
ref_row = cur.fetchone()
ref_answer = ref_row[0] if ref_row else "<NO EXCELLENT ANSWER>"
print("Excellent reference answer (first 200 chars):", ref_answer[:200])

# Test answer (same as used in earlier test)
test_answer = (
    "Denormalization duplicates data to avoid joins, improving read performance "
    "but risking consistency issues. It’s a trade‑off between speed and storage."
)

# 3. Score and raw similarity
label, sim = score_answer(110, test_answer)
print("Score label:", label)
print("Raw similarity (rounded to 4dp):", sim)

# 4. Embedding lengths and raw cosine
ref_emb = get_embedding(ref_answer)
test_emb = get_embedding(test_answer)
print("Embedding length (reference):", len(ref_emb))
print("Embedding length (test answer):", len(test_emb))

import numpy as np

def cosine(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

raw_cos = cosine(test_emb, ref_emb)
print("Raw cosine similarity (unrounded):", raw_cos)

conn.close()
