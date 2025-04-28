import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import json

DATABASE = 'parwaaz.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            xp INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        questions_json TEXT,
        user_answers_json TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

    db.commit()
    db.close()

def create_user(username, password):
    db = get_db()
    cursor = db.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    db.commit()
    db.close()

def verify_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    db.close()
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    db.close()
    return user

def save_quiz_result(user_id, score, total_questions, questions, user_answers):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO quiz_results (user_id, score, total_questions, questions_json, user_answers_json)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, score, total_questions, json.dumps(questions), json.dumps(user_answers)))
    db.commit()
    db.close()


def get_quiz_history(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM quiz_results WHERE user_id = ? ORDER BY date_time DESC', (user_id,))
    history = cursor.fetchall()
    db.close()
    return history

def add_xp(user_id, xp_gained):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE users SET xp = xp + ? WHERE id = ?', (xp_gained, user_id))
    db.commit()
    db.close()

def get_leaderboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT username, xp FROM users ORDER BY xp DESC LIMIT 5')
    leaderboard = cursor.fetchall()
    db.close()
    return leaderboard

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user

def check_password(stored_hash, password_attempt):
    return check_password_hash(stored_hash, password_attempt)