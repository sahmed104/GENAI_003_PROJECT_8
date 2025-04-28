import os
from flask import Flask
from dotenv import load_dotenv
from .models import init_db

def create_app():
    load_dotenv()

    # Force Flask to use absolute path to templates folder
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')  # Add this line

    from .routes import main
    app.register_blueprint(main)

    return app
