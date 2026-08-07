from pathlib import Path
from dotenv import load_dotenv
import os

# Project Root (AI-EdTech)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")


class Settings:
    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # MongoDB
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # Storage
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    # ChromaDB
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")


settings = Settings()