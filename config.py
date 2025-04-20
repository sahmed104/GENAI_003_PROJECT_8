import os

class Config:
    DEBUG = True
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
