from flask import Blueprint, render_template, request, session, jsonify
from .prompts import generate_summary_prompt, generate_quiz_prompt, generate_flashcard_prompt
from .openai_client import ask_openai
import os, re
from flask import current_app
import concurrent.futures

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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
