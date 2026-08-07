from fastapi import APIRouter, HTTPException

from app.models.quiz_model import QuizRequest
from app.services.quiz_service import quiz_service

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@router.post("/generate")
def generate_quiz(request: QuizRequest):

    try:
        quiz = quiz_service.generate_quiz(
            subject=request.subject,
            course=request.course,
            lesson=request.lesson,
            number_of_questions=request.number_of_questions
        )

        return {
            "success": True,
            "quiz": quiz
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )