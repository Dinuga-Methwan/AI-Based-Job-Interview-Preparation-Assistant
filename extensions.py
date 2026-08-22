import os
import sqlite3
from flask import g
from flask_login import LoginManager, UserMixin
from functools import wraps

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
QUESTIONS_PER_SESSION = 5

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'

def get_db():
    """Get a SQLite database connection, stored in Flask's application context `g`."""
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    row = db.execute(
        "SELECT id, username, password_hash, role FROM Users WHERE id = ?",
        (user_id,)
    ).fetchone()
    if row:
        return User(row['id'], row['username'], row['password_hash'], row['role'])
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask_login import current_user
        if not current_user.is_authenticated or current_user.role != 'admin':
            return login_manager.unauthorized()
        return f(*args, **kwargs)
    return decorated_function
