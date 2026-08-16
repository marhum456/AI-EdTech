from fastapi import APIRouter, HTTPException

from app.models.quiz_model import QuizRequest
from app.models.submit_quiz_model import SubmitQuizRequest
from app.services.quiz_service import quiz_service


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


# -------------------------------------------------
# Generate Quiz
# -------------------------------------------------

@router.post("/generate")
def generate_quiz(request: QuizRequest):

    try:
        result = quiz_service.generate_quiz(
            subject=request.subject,
            course=request.course,
            lesson=request.lesson,
            number_of_questions=request.number_of_questions,
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -------------------------------------------------
# Submit Quiz
# -------------------------------------------------

@router.post("/submit")
def submit_quiz(request: SubmitQuizRequest):

    try:
        result = quiz_service.submit_quiz(
            quiz_id=request.quiz_id,
            answers=[answer.model_dump() for answer in request.answers],
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )