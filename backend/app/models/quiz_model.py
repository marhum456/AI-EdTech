from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    subject: str = Field(..., example="javascript")
    course: str = Field(..., example="javascript_fundamentals")
    lesson: str = Field(..., example="lesson_1")
    number_of_questions: int = Field(default=5, ge=1, le=50)