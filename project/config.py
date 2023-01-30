import os

from dotenv import load_dotenv

current_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv()


class Config:
    DEBUG = True
    SUDO_PASSWORD = os.getenv('SUDO_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
