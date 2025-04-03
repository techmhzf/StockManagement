import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "stock_management.db"

class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, DB_NAME)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
