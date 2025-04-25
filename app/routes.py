from flask import Blueprint, request, jsonify, render_template
from .prompts import generate_summary_prompt, generate_quiz_prompt, generate_flashcard_prompt
from .openai_client import ask_openai
import os
from flask import current_app
import concurrent.futures

main = Blueprint('main', __name__)

@main.route('/test')
def test():
    return "<h1>Hello, Flask is working!</h1>"

@main.route('/')
def index():
    print("TEMPLATE FOLDER:", current_app.template_folder)
    print("FILES:", os.listdir(current_app.template_folder))
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    data = request.json
    grade = data.get('grade')
    subject = data.get('subject')
    user_prompt = data.get('prompt')

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
