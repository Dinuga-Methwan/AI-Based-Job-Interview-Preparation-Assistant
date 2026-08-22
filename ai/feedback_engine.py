import random
from ai.nlp_processor import extract_keywords, clean_text

# Rule-based feedback dictionary containing multiple distinct messages per label & category group
FEEDBACK_RULES = {
    'Excellent': {
        'default': [
            "Outstanding response! You clearly demonstrated expertise, structure, and relevant terminology.",
            "Exceptional answer! You addressed the core concept thoroughly with great clarity and accuracy.",
            "Top-tier explanation! Your response was concise, comprehensive, and hit all key details."
        ],
        'Technical': [
            "Excellent technical depth! You accurately explained core principles and key mechanisms with precision.",
            "Brilliant response! You demonstrated strong architectural awareness and clear domain knowledge.",
            "Superb answer! Your technical reasoning was spot-on and well-articulated."
        ],
        'Behavioral': [
            "Masterful behavioral answer! Excellent use of the STAR method to demonstrate real-world impact.",
            "Fantastic response! You effectively highlighted leadership, problem-solving, and personal ownership.",
            "Great storytelling! Your example was specific, impactful, and clearly showcased your soft skills."
        ]
    },
    'Good': {
        'default': [
            "Solid response! You covered the main points well. Adding a brief real-world example could make it excellent.",
            "Good job! Your explanation was clear and correct. Consider expanding slightly on key trade-offs.",
            "Well answered! You demonstrated a good understanding. Elaborating on edge cases will elevate your score."
        ],
        'Technical': [
            "Good technical explanation! To reach 'Excellent', try mentioning specific performance or implementation trade-offs.",
            "Strong understanding shown! Elaborating on underlying mechanics or memory/time complexity would enhance this answer.",
            "Clear technical response! Consider adding a concrete code or system architecture scenario."
        ],
        'Behavioral': [
            "Good answer! Try structuring your response more tightly around Situation, Task, Action, and Result (STAR).",
            "Strong response! Emphasizing quantifiable results or key lessons learned would make this even stronger.",
            "Great example provided! Make sure to highlight your specific individual contribution more clearly."
        ]
    },
    'Average': {
        'default': [
            "Decent effort, but your answer lacks depth. Try to provide specific details and structured explanations.",
            "Fair attempt. Your response addresses the question surface-level—work on articulating key definitions clearly.",
            "Moderate response. Focus on giving complete explanations rather than brief summary statements."
        ],
        'Technical': [
            "Your technical explanation is somewhat surface-level. Include specific syntax, components, or fundamental definitions.",
            "Partial understanding demonstrated. Focus on explaining 'why' and 'how', not just 'what'.",
            "Average response. Review standard technical definitions and practice explaining step-by-step implementations."
        ],
        'Behavioral': [
            "Your answer is a bit generic. Use a concrete past experience with specific actions and clear results.",
            "Average behavioral answer. Avoid general statements and focus on a single, clear STAR story.",
            "Decent context, but the outcome wasn't clear. Always explain the measurable impact of your actions."
        ]
    },
    'Poor': {
        'default': [
            "Your answer was too vague or incomplete. Re-study the core concept and practice structuring a complete response.",
            "Needs significant improvement. Make sure to directly address the prompt with factual and relevant details.",
            "Unclear response. Take time to review key terminology and prepare structured talking points."
        ],
        'Technical': [
            "Inaccurate or missing key technical concepts. We recommend revising fundamental topics in this category.",
            "Your response missed essential technical definitions. Focus on learning core principles before interviewing.",
            "Incomplete technical answer. Practice defining key terms clearly and outlining solution approaches."
        ],
        'Behavioral': [
            "Your response lacked a clear real-world scenario. Prepare 2-3 structured stories using the STAR method.",
            "Weak response. Avoid vague statements like 'I usually handle it well'—describe specific actions you took.",
            "Missing key behavioral components. Clearly outline the Situation, your specific Action, and the final Result."
        ]
    }
}

TECHNICAL_CATEGORIES = {
    'General Programming', 'Data Structures', 'Languages and Frameworks', 
    'Database and SQL', 'Web Development', 'Software Testing', 
    'Version Control', 'System Design', 'Algorithms', 'Technical'
}

BEHAVIORAL_CATEGORIES = {
    'Adaptability', 'Conflict Resolution', 'Career Goals', 
    'Team Collaboration', 'Culture Fit', 'Motivation', 
    'Leadership', 'Work Style', 'Behavioral'
}

def get_feedback(label: str, category: str = None) -> str:
    """
    Given a score label (Poor/Average/Good/Excellent) and an optional category (e.g., Leadership, System Design),
    returns a specific piece of written feedback advice.
    """
    if not label:
        normalized_label = 'Average'
    else:
        normalized_label = label.strip().capitalize()

    if normalized_label not in FEEDBACK_RULES:
        normalized_label = 'Average'
        
    label_rules = FEEDBACK_RULES[normalized_label]
    
    # Categorize into Technical, Behavioral, or default
    category_group = 'default'
    if category:
        cat_clean = category.strip()
        if cat_clean in TECHNICAL_CATEGORIES or any(kw in cat_clean.lower() for kw in ['tech', 'design', 'code', 'prog', 'sql', 'algo']):
            category_group = 'Technical'
        elif cat_clean in BEHAVIORAL_CATEGORIES or any(kw in cat_clean.lower() for kw in ['lead', 'behavior', 'team', 'culture', 'conflict']):
            category_group = 'Behavioral'
    
    options = label_rules.get(category_group, label_rules['default'])
    return random.choice(options)

def get_next_difficulty(current_difficulty: str, score_label: str) -> str:
    """Determine the next difficulty level based on current difficulty and score.
    
    Args:
        current_difficulty: One of 'Easy', 'Medium', 'Hard'.
        score_label: Score label such as 'Excellent', 'Good', 'Average', 'Poor'.
    Returns:
        New difficulty level as a string.
    """
    # Normalize inputs
    cur = current_difficulty.strip().capitalize()
    label = score_label.strip().capitalize()
    order = ['Easy', 'Medium', 'Hard']
    if label in ('Excellent', 'Good'):
        # Move up one level, max Hard
        if cur != 'Hard':
            return order[order.index(cur) + 1]
        return 'Hard'
    elif label in ('Poor', 'Average'):
        # Move down one level, min Easy
        if cur != 'Easy':
            return order[order.index(cur) - 1]
        return 'Easy'
    # No change for unexpected labels
    return cur

def get_missing_concepts(question_id: int, user_answer: str, db_path: str = None) -> list:
    """Return reference keywords that truly do NOT appear in the user's answer.
    Steps:
    1. Load the Excellent reference answer for the given question.
    2. Extract top‑N keywords from that reference answer (using extract_keywords).
    3. Clean the full user answer text.
    4. For each reference keyword, if it is NOT a substring of the cleaned user answer, include it.
    5. Return up to 4 missing concepts, preserving TF‑IDF order.
    """
    # Resolve DB path (same logic as scorer)
    if db_path is None:
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'database.db')
        if not os.path.exists(db_path):
            db_path = 'database.db'
    import sqlite3
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT answer_text FROM ReferenceAnswers
        WHERE question_id = ? AND label = 'Excellent'
        """,
        (question_id,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return []
    ref_answer = row[0]
    # Extract keywords from reference answer
    ref_keywords = extract_keywords(ref_answer)
    # Clean user's full answer for substring matching
    cleaned_user = clean_text(user_answer)
    missing = []
    for kw in ref_keywords:
        if kw not in cleaned_user:
            missing.append(kw)
        if len(missing) >= 4:
            break
    return missing

if __name__ == '__main__':
    # Simple sanity test for the new function
    q_id = 110
    user_ans = (
        "Denormalization duplicates data to avoid joins, improving read performance "
        "but risking consistency issues. It’s a trade‑off between speed and storage."
    )
    print('Missing concepts:', get_missing_concepts(q_id, user_ans))
    
    test_cases = [
        ("Excellent", "System Design"),
        ("Good", "Leadership"),
        ("Average", "General Programming"),
        ("Poor", "Conflict Resolution"),
        ("Excellent", "Unknown Category")
    ]
    
    print("--- Feedback Engine Test Output ---")
    for score_label, cat in test_cases:
        feedback = get_feedback(score_label, cat)
        print(f"[{score_label}] Category: '{cat}'")
        print(f"Advice: \"{feedback}\"\n")
