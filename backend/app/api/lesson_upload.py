from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.lesson_upload_service import lesson_upload_service


# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/admin/lessons",
    tags=["Admin Lessons"]
)


# =====================================================
# Upload Lesson PDF
# =====================================================

@router.post("/upload")
async def upload_lesson(
    subject: str = Form(...),
    course: str = Form(...),
    lesson: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a lesson PDF.

    Receives:
        subject -> Subject name
        course  -> Course name
        lesson  -> Lesson identifier
        file    -> Lesson PDF

    The service handles:
        1. PDF validation
        2. PDF saving
        3. Text extraction
        4. Chunk creation
        5. Embedding generation
        6. ChromaDB storage
    """

    try:

        # -------------------------------------------------
        # Validate PDF
        # -------------------------------------------------

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file was provided."
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        # -------------------------------------------------
        # Log received information
        # -------------------------------------------------

        print("\n===================================")
        print("LESSON UPLOAD REQUEST:")
        print(f"Subject = {subject}")
        print(f"Course  = {course}")
        print(f"Lesson  = {lesson}")
        print(f"File    = {file.filename}")
        print("===================================\n")

        # -------------------------------------------------
        # Send to upload service
        # -------------------------------------------------

        result = await lesson_upload_service.upload_lesson(
            subject=subject,
            course=course,
            lesson=lesson,
            file=file
        )

        # -------------------------------------------------
        # Return success response
        # -------------------------------------------------

        return {
            "message": "Lesson uploaded successfully.",
            "subject": subject,
            "course": course,
            "lesson": lesson,
            "filename": file.filename,
            "result": result
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"❌ Lesson upload error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )