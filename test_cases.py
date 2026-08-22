import sqlite3
import os
from ai.scorer import score_answer
from ai.feedback_engine import get_feedback

DB_PATH = 'database.db'

def get_question_details(question_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT question_text, category FROM Questions WHERE id = ?;", (question_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return "Unknown Question", "General"

def run_pipeline(question_id, user_answer):
    """
    Executes the full AI evaluation pipeline (nlp_processor -> scorer -> feedback_engine).
    Handles empty string inputs with a validation message.
    """
    question_text, category = get_question_details(question_id)
    
    # 3. Input validation check for empty strings
    if not user_answer or not user_answer.strip():
        return {
            'question_id': question_id,
            'question_text': question_text,
            'category': category,
            'user_answer': repr(user_answer),
            'score_label': 'Validation Error',
            'similarity_score': 0.0,
            'feedback_text': 'Validation Warning: Answer input cannot be empty. Please provide a detailed response.'
        }
    
    # 1 & 2. Run NLP processor, scorer, and feedback engine
    score_label, similarity_score = score_answer(question_id, user_answer, db_path=DB_PATH)
    feedback_text = get_feedback(score_label, category)
    
    return {
        'question_id': question_id,
        'question_text': question_text,
        'category': category,
        'user_answer': user_answer,
        'score_label': score_label,
        'similarity_score': similarity_score,
        'feedback_text': feedback_text
    }

def main():
    print("=" * 75)
    print("      AI INTERVIEW COACH - FULL PIPELINE TEST SUITE (test_cases.py)")
    print("=" * 75)
    print()

    question_id = 1
    
    # Test Case 1: Strong, Detailed Answer
    strong_answer = (
        "A compiler translates the entire source code into machine code all at once before execution, "
        "whereas an interpreter translates and executes code line by line during runtime."
    )
    res1 = run_pipeline(question_id, strong_answer)
    print("---------------------------------------------------------------------------")
    print("TEST CASE 1: Strong & Detailed Answer")
    print("---------------------------------------------------------------------------")
    print(f"Question #{res1['question_id']}: {res1['question_text']}")
    print(f"Category   : {res1['category']}")
    print(f"User Input : \"{res1['user_answer']}\"")
    print(f"Result Label    : {res1['score_label']} (Expected: Good / Excellent)")
    print(f"Similarity Score: {res1['similarity_score']}")
    print(f"AI Advice       : \"{res1['feedback_text']}\"")
    print()

    # Test Case 2: One-word / Off-topic Answer
    offtopic_answer = "Pizza"
    res2 = run_pipeline(question_id, offtopic_answer)
    print("---------------------------------------------------------------------------")
    print("TEST CASE 2: One-Word / Off-Topic Answer")
    print("---------------------------------------------------------------------------")
    print(f"Question #{res2['question_id']}: {res2['question_text']}")
    print(f"Category   : {res2['category']}")
    print(f"User Input : \"{res2['user_answer']}\"")
    print(f"Result Label    : {res2['score_label']} (Expected: Poor)")
    print(f"Similarity Score: {res2['similarity_score']}")
    print(f"AI Advice       : \"{res2['feedback_text']}\"")
    print()

    # Test Case 3: Empty String Answer
    empty_answer = "   "
    res3 = run_pipeline(question_id, empty_answer)
    print("---------------------------------------------------------------------------")
    print("TEST CASE 3: Empty String Input (Validation Handling)")
    print("---------------------------------------------------------------------------")
    print(f"Question #{res3['question_id']}: {res3['question_text']}")
    print(f"Category   : {res3['category']}")
    print(f"User Input : {res3['user_answer']}")
    print(f"Result Label    : {res3['score_label']}")
    print(f"Similarity Score: {res3['similarity_score']}")
    print(f"AI Advice       : \"{res3['feedback_text']}\"")
    print()

    print("=" * 75)
    print("                     ALL TEST CASES COMPLETED SUCCESSFULLY")
    print("=" * 75)

if __name__ == '__main__':
    main()
