from fastapi import FastAPI
from app.config import settings
from contextlib import asynccontextmanager
from app.api.quiz import router as quiz_router

from app.database.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
)

from contextlib import asynccontextmanager
from app.database.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
)

@asynccontextmanager
async def lifespan(app):
    # Startup
    connect_to_mongodb()

    yield

    # Shutdown
    close_mongodb_connection()


app = FastAPI(
    title="AI EdTech API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(quiz_router)

@app.get("/")
def root():
    return {
        "message": "AI EdTech API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "message": "Server is healthy"
    }

print("\n===== Project Configuration =====")
print(f"MongoDB URI    : {settings.MONGODB_URI}")
print(f"Database Name  : {settings.DATABASE_NAME}")
print(f"Upload Folder  : {settings.UPLOAD_FOLDER}")
print(f"ChromaDB Path  : {settings.CHROMA_DB_PATH}")
print("=================================\n")