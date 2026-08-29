import os
from flask import send_from_directory, abort
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from ai.scorer import score_answer
from ai.feedback_engine import get_next_difficulty
from ai.feedback_engine import get_feedback
from extensions import get_db, User, admin_required, DB_PATH, QUESTIONS_PER_SESSION, login_manager
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all API routes
CORS(app, resources={r'/api/*': {'origins': '*'}}, supports_credentials=True)
app.secret_key = 'ai-interview-coach-secret-key'
login_manager.init_app(app)

# Database cleanup

def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize user table

def init_user_table():
    """Create Users table if it does not already exist."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()

with app.app_context():
    init_user_table()

# Register API blueprint with /api prefix
from api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')


@app.route('/')
def landing():
    """Public marketing landing page (no login required)."""
    return render_template('landing.html', current_year=datetime.now().year)

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    
    # Total completed interview sessions for this user (only count sessions that have at least 1 answer)
    interviews_completed = db.execute("""
        SELECT COUNT(DISTINCT s.id) FROM Sessions s
        JOIN UserAnswers ua ON ua.session_id = s.id
        WHERE s.user_id = ?
    """, (current_user.id,)).fetchone()[0]
    
    # Average score across all this user's answers
    score_map = {'Excellent': 100, 'Good': 80, 'Average': 55, 'Poor': 25}
    rows = db.execute("""
        SELECT ua.score_label FROM UserAnswers ua
        JOIN Sessions s ON ua.session_id = s.id
        WHERE s.user_id = ?
    """, (current_user.id,)).fetchall()
    scores = [score_map.get(r['score_label'], 0) for r in rows]
    average_score = round(sum(scores) / len(scores)) if scores else 0
    
    # Recent sessions with their own average score, most recent first, only ones with answers
    recent_sessions_raw = db.execute("""
        SELECT s.id, s.job_role, s.created_at, COUNT(ua.id) as question_count
        FROM Sessions s
        JOIN UserAnswers ua ON ua.session_id = s.id
        WHERE s.user_id = ?
        GROUP BY s.id
        ORDER BY s.created_at DESC
        LIMIT 5
    """, (current_user.id,)).fetchall()
    
    recent_sessions = []
    for s in recent_sessions_raw:
        session_scores = db.execute("""
            SELECT score_label FROM UserAnswers WHERE session_id = ?
        """, (s['id'],)).fetchall()
        s_scores = [score_map.get(r['score_label'], 0) for r in session_scores]
        s_avg = round(sum(s_scores) / len(s_scores)) if s_scores else 0
        recent_sessions.append({
            'id': s['id'], 'job_role': s['job_role'], 'created_at': s['created_at'],
            'question_count': s['question_count'], 'average_score': s_avg
        })
    
    return render_template('dashboard.html',
        interviews_completed=interviews_completed,
        average_score=average_score,
        recent_sessions=recent_sessions)

# ---------- Authentication routes ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password required.', 'error')
            return render_template('register.html')
        db = get_db()
        existing = db.execute('SELECT id FROM Users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Username already taken.', 'error')
            return render_template('register.html')
        password_hash = generate_password_hash(password)
        db.execute('INSERT INTO Users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                   (username, email, password_hash, 'user'))
        db.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        user_row = db.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
        if user_row and check_password_hash(user_row['password_hash'], password):
            user = User(user_row['id'], user_row['username'], user_row['password_hash'], user_row['role'])
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ---------- Admin dashboard ----------
@app.route('/admin')
@admin_required
def admin_dashboard():
    db = get_db()
    users = db.execute('SELECT id, username, email, role, created_at FROM Users').fetchall()
    return render_template('admin.html', users=users)


@app.route('/interview')
@login_required
def interview():
    """
    Starts or continues an interview session.
    Shows one question at a time for the selected job role.
    """
    role = request.args.get('role', 'Software Engineer')
    session_id = request.args.get('session_id', type=int)

    db = get_db()

    if not session_id:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Sessions (job_role, user_id) VALUES (?, ?);", (role, current_user.id))
        db.commit()
        session_id = cursor.lastrowid
        return redirect(url_for('interview', role=role, session_id=session_id))

    session_row = db.execute("SELECT current_difficulty FROM Sessions WHERE id = ?;", (session_id,)).fetchone()
    current_difficulty = session_row['current_difficulty'] if session_row else 'Medium'

    print(f"[DEBUG] Session {session_id} current difficulty: {current_difficulty}")

    answered_count = db.execute(
        "SELECT COUNT(*) FROM UserAnswers WHERE session_id = ?;",
        (session_id,)
    ).fetchone()[0]

    if answered_count >= QUESTIONS_PER_SESSION:
        return redirect(url_for('report', session_id=session_id))

    def fetch_question(diff):
        print(f"[DEBUG] Selecting next question with difficulty filter: {diff}")
        return db.execute("""
            SELECT id, job_role, question_type, category, question_text 
            FROM Questions 
            WHERE job_role = ? AND difficulty = ? AND id NOT IN (
                SELECT question_id FROM UserAnswers WHERE session_id = ?
            )
            ORDER BY RANDOM() 
            LIMIT 1;
        """, (role, diff, session_id)).fetchone()

    question_row = fetch_question(current_difficulty)
    if not question_row:
        difficulties = ['Easy', 'Medium', 'Hard']
        idx = difficulties.index(current_difficulty)
        fallback_order = [d for i, d in enumerate(difficulties) if i != idx]
        for diff in fallback_order:
            question_row = fetch_question(diff)
            if question_row:
                break

    if not question_row:
        return redirect(url_for('report', session_id=session_id))

    question = {
        'id': question_row['id'],
        'job_role': question_row['job_role'],
        'question_type': question_row['question_type'],
        'category': question_row['category'],
        'question_text': question_row['question_text']
    }

    return render_template(
        'interview.html',
        role=role,
        session_id=session_id,
        question=question,
        current_num=answered_count + 1,
        total_questions=QUESTIONS_PER_SESSION
    )


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """
    Handles user answer submission.
    """
    session_id = request.form.get('session_id', type=int)
    question_id = request.form.get('question_id', type=int)
    answer_text = request.form.get('answer_text', '').strip()

    db = get_db()

    q_row = db.execute("SELECT id, job_role, question_type, category, question_text FROM Questions WHERE id = ?;", (question_id,)).fetchone()
    s_row = db.execute("SELECT job_role FROM Sessions WHERE id = ?;", (session_id,)).fetchone()

    if not q_row or not s_row:
        return redirect(url_for('dashboard'))

    category = q_row['category']
    role = s_row['job_role']

    words = answer_text.split()
    if len(words) < 3:
        answered_count = db.execute(
            "SELECT COUNT(*) FROM UserAnswers WHERE session_id = ?;", (session_id,)
        ).fetchone()[0]

        question = {
            'id': q_row['id'],
            'job_role': q_row['job_role'],
            'question_type': q_row['question_type'],
            'category': q_row['category'],
            'question_text': q_row['question_text']
        }

        return render_template(
            'interview.html',
            role=role,
            session_id=session_id,
            question=question,
            current_num=answered_count + 1,
            total_questions=QUESTIONS_PER_SESSION,
            error_message="Please provide a more complete answer (at least 3 words) before submitting.",
            previous_answer=answer_text
        )

    score_label, similarity_score = score_answer(question_id, answer_text, db_path=DB_PATH)
    feedback_text = get_feedback(score_label, category)

    db.execute("""
        INSERT INTO UserAnswers (session_id, question_id, answer_text, score_label, feedback_text)
        VALUES (?, ?, ?, ?, ?);
    """, (session_id, question_id, answer_text, score_label, feedback_text))

    current_diff = db.execute("SELECT current_difficulty FROM Sessions WHERE id = ?;", (session_id,)).fetchone()['current_difficulty']
    new_difficulty = get_next_difficulty(current_diff, score_label)
    db.execute("UPDATE Sessions SET current_difficulty = ? WHERE id = ?;", (new_difficulty, session_id))
    db.commit()

    updated_diff = db.execute("SELECT current_difficulty FROM Sessions WHERE id = ?;", (session_id,)).fetchone()['current_difficulty']
    print(f"[DEBUG] Session {session_id}: Updated difficulty to {updated_diff}")

    answered_count = db.execute(
        "SELECT COUNT(*) FROM UserAnswers WHERE session_id = ?;",
        (session_id,)
    ).fetchone()[0]

    if answered_count >= QUESTIONS_PER_SESSION:
        return redirect(url_for('report', session_id=session_id))

    return redirect(url_for('interview', role=role, session_id=session_id))

@app.route('/report/<int:session_id>')
def report(session_id):
    """
    Displays the interview session performance report.
    """
    db = get_db()

    session_row = db.execute(
        "SELECT id, job_role, created_at FROM Sessions WHERE id = ?;", (session_id,)
    ).fetchone()

    if not session_row:
        return redirect(url_for('dashboard'))

    session_data = {
        'id': session_row['id'],
        'job_role': session_row['job_role'],
        'created_at': session_row['created_at']
    }

    user_answers = db.execute("""
        SELECT u.question_id, q.question_text, q.category, q.difficulty, u.answer_text, u.score_label, u.feedback_text
        FROM UserAnswers u
        JOIN Questions q ON u.question_id = q.id
        WHERE u.session_id = ?
        ORDER BY u.id ASC;
    """, (session_id,)).fetchall()

    answers_list = [dict(row) for row in user_answers]

    stats = {'excellent': 0, 'good': 0, 'average': 0, 'poor': 0}
    for ans in answers_list:
        label = (ans['score_label'] or '').lower()
        if label in stats:
            stats[label] += 1
        else:
            stats['poor'] += 1

    return render_template(
        'report.html',
        session_data=session_data,
        answers=answers_list,
        stats=stats
    )


# ---------- React frontend, served at /app (kept separate from '/' to avoid route conflicts) ----------
REACT_DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'dist')

@app.route('/app')
@app.route('/app/<path:subpath>')
def react_app(subpath=''):
    return send_from_directory(REACT_DIST_DIR, 'index.html')

@app.route('/assets/<path:filename>')
def react_assets(filename):
    return send_from_directory(os.path.join(REACT_DIST_DIR, 'assets'), filename)
with app.app_context():
    print('REGISTERED ROUTES:')
    for rule in app.url_map.iter_rules():
        print(rule, rule.methods)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=5000)