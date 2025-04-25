import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    # Force Flask to use absolute path to templates folder
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    from .routes import main
    app.register_blueprint(main)

    return app
