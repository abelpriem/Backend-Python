import os
from dotenv import load_dotenv

load_dotenv() # Carga variables desde el .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")
    DEBUG = os.getenv("DEBUG", True)
    DB_URL = os.getenv("DATABASE_URL")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))