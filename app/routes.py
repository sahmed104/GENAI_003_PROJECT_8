from flask import Blueprint, request, jsonify, render_template
from .prompts import generate_summary_prompt, generate_quiz_prompt, generate_flashcard_prompt
from .openai_client import ask_openai

main = Blueprint('main', __name__)

@main.route('/test')
def test():
    return "<h1>Hello, Flask is working!</h1>"

import os
from flask import current_app

@main.route('/')
def index():
    print("TEMPLATE FOLDER:", current_app.template_folder)
    print("FILES:", os.listdir(current_app.template_folder))
    return render_template('index.html')


# API route to handle POST request for generation
@main.route('/generate', methods=['POST'])
def generate():
    data = request.json
    grade = data.get('grade')
    subject = data.get('subject')
    user_prompt = data.get('prompt')

    quiz_type = data.get('quiz_type', 'mcq')
    quiz_count = int(data.get('quiz_count', 3))  # from user
    flashcard_count = int(data.get('flashcard_count', 3))  # from user

    summary_prompt = generate_summary_prompt(grade, subject, user_prompt)
    quiz_prompt = generate_quiz_prompt(grade, subject, user_prompt, quiz_type, quiz_count)
    flash_prompt = generate_flashcard_prompt(grade, subject, user_prompt, flashcard_count)

    summary = ask_openai(summary_prompt)
    quiz = ask_openai(quiz_prompt)
    flashcards = ask_openai(flash_prompt)

    return jsonify({
        "summary": summary,
        "quiz": quiz,
        "flashcards": flashcards
    })