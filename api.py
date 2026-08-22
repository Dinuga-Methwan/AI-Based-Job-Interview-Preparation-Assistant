from flask import Blueprint, request, jsonify, abort
from extensions import get_db, login_manager, User, admin_required, QUESTIONS_PER_SESSION, DB_PATH
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from ai.scorer import score_answer
from ai.feedback_engine import get_feedback, get_next_difficulty

api_bp = Blueprint('api', __name__)

# Helper to serialize user
def _user_dict(user_row):
    return {
        "id": user_row["id"],
        "username": user_row["username"],
        "role": user_row["role"]
    }

@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"success": False, "error": "Missing credentials"}), 400
    db = get_db()
    row = db.execute("SELECT id, username, password_hash, role FROM Users WHERE username = ?", (username,)).fetchone()
    if row and check_password_hash(row['password_hash'], password):
        user = User(row['id'], row['username'], row['password_hash'], row['role'])
        login_user(user)
        return jsonify({"success": True, "user": _user_dict(row)})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@api_bp.route('/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    db = get_db()
    existing = db.execute('SELECT id FROM Users WHERE username = ?', (username,)).fetchone()
    if existing:
        return jsonify({"error": "Username already taken"}), 409
    password_hash = generate_password_hash(password)
    db.execute('INSERT INTO Users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
               (username, email, password_hash, 'user'))
    db.commit()
    return jsonify({"success": True})

@api_bp.route('/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({"success": True})

@api_bp.route('/me', methods=['GET'])
def api_me():
    if not current_user.is_authenticated:
        return abort(401)
    return jsonify({"id": current_user.id, "username": current_user.username, "role": current_user.role})

@api_bp.route('/roles', methods=['GET'])
def api_roles():
    db = get_db()
    rows = db.execute('SELECT DISTINCT job_role FROM Questions').fetchall()
    roles = [r['job_role'] for r in rows]
    return jsonify({"roles": roles})

@api_bp.route('/interview/start', methods=['POST'])
@login_required
def api_interview_start():
    data = request.get_json() or {}
    role = data.get('job_role') or 'Software Engineer'
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO Sessions (job_role) VALUES (?);', (role,))
    db.commit()
    session_id = cursor.lastrowid
    # reuse existing interview logic to fetch first question
    current_difficulty = 'Medium'
    def fetch_question(diff):
        return db.execute('''
            SELECT id, job_role, question_type, category, question_text FROM Questions
            WHERE job_role = ? AND difficulty = ? AND id NOT IN (
                SELECT question_id FROM UserAnswers WHERE session_id = ?
            ) ORDER BY RANDOM() LIMIT 1;''', (role, diff, session_id)).fetchone()
    question_row = fetch_question(current_difficulty)
    if not question_row:
        return jsonify({"error": "No questions available"}), 404
    question = {
        "id": question_row['id'],
        "job_role": question_row['job_role'],
        "question_type": question_row['question_type'],
        "category": question_row['category'],
        "question_text": question_row['question_text']
    }
    return jsonify({
        "session_id": session_id,
        "question": question,
        "difficulty": current_difficulty,
        "question_number": 1,
        "total_questions": QUESTIONS_PER_SESSION
    })

@api_bp.route('/interview/answer', methods=['POST'])
@login_required
def api_interview_answer():
    data = request.get_json() or {}
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    answer_text = data.get('answer_text', '').strip()
    if not all([session_id, question_id, answer_text]):
        return jsonify({"error": "Missing fields"}), 400
    db = get_db()
    q_row = db.execute('SELECT id, job_role, question_type, category, question_text FROM Questions WHERE id = ?;', (question_id,)).fetchone()
    s_row = db.execute('SELECT job_role FROM Sessions WHERE id = ?;', (session_id,)).fetchone()
    if not q_row or not s_row:
        return jsonify({"error": "Invalid session or question"}), 404
    category = q_row['category']
    # Scoring and feedback
    score_label, similarity_score = score_answer(question_id, answer_text, db_path=DB_PATH)
    feedback_text = get_feedback(score_label, category)
    # Save answer
    db.execute('''
        INSERT INTO UserAnswers (session_id, question_id, answer_text, score_label, feedback_text)
        VALUES (?, ?, ?, ?, ?);
    ''', (session_id, question_id, answer_text, score_label, feedback_text))
    # Update difficulty
    current_diff = db.execute('SELECT current_difficulty FROM Sessions WHERE id = ?;', (session_id,)).fetchone()['current_difficulty']
    new_difficulty = get_next_difficulty(current_diff, score_label)
    db.execute('UPDATE Sessions SET current_difficulty = ? WHERE id = ?;', (new_difficulty, session_id))
    db.commit()
    # Determine next question
    answered_count = db.execute('SELECT COUNT(*) FROM UserAnswers WHERE session_id = ?;', (session_id,)).fetchone()[0]
    if answered_count >= QUESTIONS_PER_SESSION:
        next_q = None
    else:
        # reuse fetch_question helper from start route (redefine here)
        def fetch_question(diff):
            return db.execute('''
                SELECT id, job_role, question_type, category, question_text FROM Questions
                WHERE job_role = ? AND difficulty = ? AND id NOT IN (
                    SELECT question_id FROM UserAnswers WHERE session_id = ?
                ) ORDER BY RANDOM() LIMIT 1;''', (s_row['job_role'], new_difficulty, session_id)).fetchone()
        next_row = fetch_question(new_difficulty)
        if not next_row:
            next_q = None
        else:
            next_q = {
                "id": next_row['id'],
                "job_role": next_row['job_role'],
                "question_type": next_row['question_type'],
                "category": next_row['category'],
                "question_text": next_row['question_text']
            }
    return jsonify({
        "label": score_label,
        "similarity": similarity_score,
        "feedback": feedback_text,
        "next_question": next_q,
        "new_difficulty": new_difficulty,
        "answered_count": answered_count
    })

@api_bp.route('/report/<int:session_id>', methods=['GET'])
@login_required
def api_report(session_id):
    db = get_db()
    session_row = db.execute('SELECT id, job_role, created_at FROM Sessions WHERE id = ?;', (session_id,)).fetchone()
    if not session_row:
        return jsonify({"error": "Session not found"}), 404
    user_answers = db.execute('''
        SELECT u.question_id, q.question_text, q.category, q.difficulty, u.answer_text, u.score_label, u.feedback_text
        FROM UserAnswers u JOIN Questions q ON u.question_id = q.id
        WHERE u.session_id = ? ORDER BY u.id ASC;
    ''', (session_id,)).fetchall()
    answers = [dict(row) for row in user_answers]
    return jsonify({
        "session": {
            "id": session_row['id'],
            "job_role": session_row['job_role'],
            "created_at": session_row['created_at']
        },
        "answers": answers
    })

@api_bp.route('/admin/users', methods=['GET'])
@admin_required
def api_admin_users():
    db = get_db()
    users = db.execute('SELECT id, username, email, role, created_at FROM Users').fetchall()
    user_list = [{
        "id": u['id'],
        "username": u['username'],
        "email": u['email'],
        "role": u['role'],
        "created_at": u['created_at']
    } for u in users]
    return jsonify({"users": user_list})
