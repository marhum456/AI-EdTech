from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.quiz import router as quiz_router

from app.database.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
)


# =================================================
# Project Directories
# =================================================

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOADS_DIR = BASE_DIR / "uploads"


# =================================================
# Lifespan
# =================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    connect_to_mongodb()

    yield

    close_mongodb_connection()


# =================================================
# FastAPI Application
# =================================================

app = FastAPI(
    title="AI EdTech API",
    version="1.0.0",
    lifespan=lifespan
)


# =================================================
# CORS
# =================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# =================================================
# PDF / UPLOADS
# =================================================

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads"
)


# =================================================
# API Routers
# =================================================

app.include_router(quiz_router)


# =================================================
# Root
# =================================================

@app.get("/")
def root():

    return {
        "message": "AI EdTech API is running successfully!"
    }


@app.get("/uploads/mathematics/Geometry.pdf")
def mathematics_geometry():

    from fastapi.responses import FileResponse

    pdf_path = MATH_DIR / "Mathematics- Geometry.pdf"

    return FileResponse(
        pdf_path,
        media_type="application/pdf"
    )
# =================================================
# Health
# =================================================

@app.get("/health")
def health_check():

    return {
        "status": "OK",
        "message": "Server is healthy"
    }


# =================================================
# Configuration
# =================================================

print("\n===== Project Configuration =====")

print(f"MongoDB URI    : {settings.MONGODB_URI}")
print(f"Database Name  : {settings.DATABASE_NAME}")
print(f"Upload Folder  : {settings.UPLOAD_FOLDER}")
print(f"ChromaDB Path  : {settings.CHROMA_DB_PATH}")
print(f"Project Root   : {BASE_DIR}")
print(f"Uploads Path   : {UPLOADS_DIR}")

print("=================================\n")