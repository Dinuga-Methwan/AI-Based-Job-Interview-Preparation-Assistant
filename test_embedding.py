import os
import sys

# Ensure project root is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from ai.scorer import score_answer
import sqlite3

def get_question_ids(limit=3):
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM Questions LIMIT ?", (limit,))
    ids = [row[0] for row in cur.fetchall()]
    conn.close()
    return ids

def run_tests():
    question_ids = get_question_ids(3)
    # Define answer variants (text, expected label)
    answers = [
        ("An excellent, detailed, correct answer that fully addresses the question with examples and explanations.", "Excellent"),
        ("A good answer that is correct but shorter and less detailed.", "Good"),
        ("A partially correct or vague answer that touches on some aspects.", "Average"),
        ("A topically related answer that does not actually answer the question.", "Poor"),
        ("A completely unrelated/off‑topic answer about cooking or sports.", "Poor"),
        ("", "Poor")
    ]

    results = []
    for qid in question_ids:
        for ans_text, expected in answers:
            label, sim = score_answer(qid, ans_text)
            results.append((sim, expected, qid, label))

    # sort by similarity descending
    results.sort(key=lambda x: x[0], reverse=True)

    # print table header
    print(f"{'Similarity':>10} | {'Expected':>9} | {'QuestionID':>10} | {'Predicted':>9}")
    print('-' * 50)
    for sim, expected, qid, pred in results:
        print(f"{sim:10.4f} | {expected:9} | {qid:10} | {pred:9}")

if __name__ == '__main__':
    run_tests()
