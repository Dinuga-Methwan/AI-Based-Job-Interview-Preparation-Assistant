import os
import sys
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from ai.nlp_processor import fit_vectorizer, vectorize, get_embedding

def get_db_connection(db_path=None):
    if db_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'database.db')
        if not os.path.exists(db_path):
            db_path = 'database.db'
    return sqlite3.connect(db_path)

def score_answer(question_id: int, user_answer: str, db_path: str = None):
    """
    Scores a user's submitted answer against reference answers for a given question_id.
    
    1. Loads all ReferenceAnswers (Poor/Average/Good/Excellent) for question_id from SQLite.
    2. Vectorizes both reference answers and user answer using nlp_processor.
    3. Computes cosine similarity between user's answer and each reference answer.
    4. Returns (predicted_label, similarity_score).
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT answer_text, label 
        FROM ReferenceAnswers 
        WHERE question_id = ? AND label = 'Excellent'
    """, (question_id,))
    rows = cursor.fetchall()
    # If no Excellent references, fall back to all labels
    if not rows:
        cursor.execute("""
            SELECT answer_text, label 
            FROM ReferenceAnswers 
            WHERE question_id = ?
        """, (question_id,))
        rows = cursor.fetchall()
        if not rows:
            raise ValueError(f"No reference answers found for question_id: {question_id}")
    conn.close()
    
    ref_texts = [r[0] for r in rows]
    labels = [r[1] for r in rows]
    
    # Compute embeddings for user answer and reference answers (prefer Excellent)
    user_emb = get_embedding(user_answer)
    ref_embs = [get_embedding(txt) for txt in ref_texts]
    
    # Cosine similarity helper
    def cosine_sim(a, b):
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    similarities = [cosine_sim(user_emb, ref_emb) for ref_emb in ref_embs]
    best_similarity = max(similarities)
    
    # Map similarity to label using new thresholds
    if best_similarity >= 0.75:
        predicted_label = "Excellent"
    elif best_similarity >= 0.60:
        predicted_label = "Good"
    elif best_similarity >= 0.45:
        predicted_label = "Average"
    else:
        predicted_label = "Poor"
    
    return predicted_label, round(best_similarity, 4)


if __name__ == '__main__':
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, question_text FROM Questions WHERE id = 1;")
    q_row = cursor.fetchone()
    conn.close()
    
    if q_row:
        q_id, q_text = q_row
        print(f"Testing Scorer for Question #{q_id}: '{q_text}'\n")
        
        # Test Sample 1: Good / Excellent Answer
        good_sample = "A compiler translates the entire source code into machine code before execution, while an interpreter translates code line by line at runtime."
        label_good, score_good = score_answer(q_id, good_sample)
        print(f"Sample Answer (Technical & Clear):")
        print(f"  Input: '{good_sample}'")
        print(f"  Predicted Label: {label_good}")
        print(f"  Similarity Score: {score_good}\n")
        
        # Test Sample 2: Poor Answer
        poor_sample = "I'm not really sure, I think it has something to do with writing code."
        label_poor, score_poor = score_answer(q_id, poor_sample)
        print(f"Sample Answer (Vague & Uncertain):")
        print(f"  Input: '{poor_sample}'")
        print(f"  Predicted Label: {label_poor}")
        print(f"  Similarity Score: {score_poor}\n")
    else:
        print("Question #1 not found in database. Make sure database.db is seeded.")
