from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from .prompts import generate_summary_prompt, generate_quiz_prompt, generate_flashcard_prompt
from .openai_client import ask_openai
import os, re
from flask import current_app
import concurrent.futures
from .models import create_user, verify_user, get_user_by_id, save_quiz_result, get_quiz_history, add_xp, get_leaderboard, get_user_by_username, check_password 
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', active_page='home')

@main.route('/generate', methods=['POST'])
def generate():
    data = request.json
    grade = data.get('grade')
    subject = data.get('subject')
    user_prompt = data.get('prompt')
    
    # Save last used context
    session['last_grade'] = grade
    session['last_subject'] = subject
    session['last_prompt'] = user_prompt

    quiz_type = data.get('quiz_type', 'mcq')
    quiz_count = int(data.get('quiz_count', 3))
    flashcard_count = int(data.get('flashcard_count', 3))

    # Generate prompts
    summary_prompt = generate_summary_prompt(grade, subject, user_prompt)
    quiz_prompt = generate_quiz_prompt(grade, subject, user_prompt, quiz_type, quiz_count)
    flashcard_prompt = generate_flashcard_prompt(grade, subject, user_prompt, flashcard_count)

    # Run OpenAI calls in parallel threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_summary = executor.submit(ask_openai, summary_prompt)
        future_quiz = executor.submit(ask_openai, quiz_prompt)
        future_flashcards = executor.submit(ask_openai, flashcard_prompt)

        summary = future_summary.result()
        quiz = future_quiz.result()
        flashcards = future_flashcards.result()
    return jsonify({
        "summary": summary,
        "quiz": quiz,
        "flashcards": flashcards
    })

# Take a Quiz
@main.route('/take_quiz')
def take_quiz():
    grade = session.get('last_grade')
    subject = session.get('last_subject')
    prompt = session.get('last_prompt')

    if not (grade and subject and prompt):
        return "No recent prompt found. Please generate learning content first.", 400

    return render_template('quiz.html')

@main.route('/generate_quiz', methods=['POST'])
def generate_quiz_only():
    grade = session.get('last_grade')
    subject = session.get('last_subject')
    prompt = session.get('last_prompt')

    if not (grade and subject and prompt):
        return jsonify({"error": "No previous context found"}), 400

    try:
        # Force MCQ type and 5 questions
        quiz_prompt = generate_quiz_prompt(grade, subject, prompt, quiz_type="mcq", count=5)
        quiz_text = ask_openai(quiz_prompt)

        # Parse quiz_text into structured questions + answers
        questions, answers = parse_quiz_output(quiz_text)

        combined = []
        for idx, question in enumerate(questions):
            combined.append({
                "question": question['question'],
                "options": question['options'],
                "answer": answers.get(f"Q{idx+1}")
            })

        session['quick_quiz_questions'] = combined
        session['quick_quiz_current'] = 0
        session['quick_quiz_score'] = 0

        return jsonify({"questions": combined})

    except Exception as e:
        print(f"Error generating quiz: {e}")
        return jsonify({"error": "Failed to generate quiz"}), 500

def parse_quiz_output(raw_quiz):
    questions = []
    answers = {}

    lines = raw_quiz.strip().split("\n")
    current_question = None
    current_options = []

    is_answer_section = False

    for line in lines:
        line = line.strip()
        if line.lower().startswith("answers:"):
            is_answer_section = True
            continue

        if is_answer_section:
            if line.startswith("Q"):
                parts = line.split(":")
                if len(parts) >= 2:
                    qn = parts[0].strip()
                    ans = parts[1].strip()
                    answers[qn] = ans
        else:
            if line.startswith("Q"):
                if current_question:
                    questions.append({
                        "question": current_question,
                        "options": current_options
                    })
                current_question = line.split(":", 1)[1].strip()
                current_options = []
            elif re.match(r"^[A-D]\.", line):
                current_options.append(line.strip())

    if current_question:
        questions.append({
            "question": current_question,
            "options": current_options
        })

    return questions, answers

# ⚡ Signup
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            create_user(username, password)
            return redirect(url_for('main.login'))
        except Exception as e:
            return f"Error creating user: {e}"
    return render_template('signup.html')

# ⚡ Login
from flask import flash

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('main.login'))

    return render_template('login.html', active_page='login')


# ⚡ Logout
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# ⚡ Profile Page
@main.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.login'))

    user = get_user_by_id(user_id)
    history = get_quiz_history(user_id)

    # Convert to dicts
    history = [dict(row) for row in history]

    # 🔥 Correct the timezone for New York (UTC-4)
    for quiz in history:
        if 'date_time' in quiz and quiz['date_time']:
            try:
                dt_obj = datetime.strptime(quiz['date_time'], "%Y-%m-%d %H:%M:%S")
                dt_local = dt_obj - timedelta(hours=4)  # 👈 Subtract 4 hours
                quiz['pretty_date'] = dt_local.strftime("%B %d, %Y - %I:%M %p")
            except Exception as e:
                print(f"Error parsing date: {e}")
                quiz['pretty_date'] = quiz['date_time']  # fallback if error

    level = user['xp'] // 100
    next_level_xp = 100 - (user['xp'] % 100)

    xp_value = user['xp']

    if xp_value >= 500:
        badge = "🏆 Champion"
        next_badge = "Max level reached! 🏆"
    elif xp_value >= 300:
        badge = "🥇 Achiever"
        next_badge = "Next: 🏆 Champion at 500 XP"
    elif xp_value >= 100:
        badge = "🥈 Explorer"
        next_badge = "Next: 🥇 Achiever at 300 XP"
    else:
        badge = "🥉 Newbie"
        next_badge = "Next: 🥈 Explorer at 100 XP"

    return render_template('profile.html', user=user, history=history, level=level, next_level_xp=next_level_xp, badge=badge, next_badge=next_badge, active_page='profile')

# ⚡ Save Quiz Result (AJAX call after modal quiz)
@main.route('/save_quiz_result', methods=['POST'])
def save_result():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    score = data.get('score')
    total = data.get('total')
    questions = data.get('questions')  # new
    user_answers = data.get('user_answers')  # new

    save_quiz_result(session['user_id'], score, total, questions, user_answers)
    add_xp(session['user_id'], score * 10)

    return jsonify({'message': 'Result saved'})


# ⚡ Leaderboard Page
@main.route('/leaderboard')
def leaderboard():
    top_users = get_leaderboard()

    # 🔥 Convert Rows to dicts
    top_users = [dict(user) for user in top_users]

    # 🧠 Now safe to assign badges
    def get_badge(xp):
        if xp >= 500:
            return "🏆 Champion"
        elif xp >= 300:
            return "🥇 Achiever"
        elif xp >= 100:
            return "🥈 Explorer"
        else:
            return "🥉 Newbie"

    for user in top_users:
        user['badge'] = get_badge(user['xp'])

    return render_template('leaderboard.html', top_users=top_users, active_page='leaderboard')

@main.route('/check_login_status')
def check_login_status():
    return jsonify({"logged_in": 'user_id' in session})
