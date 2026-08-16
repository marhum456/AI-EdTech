from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    question: int
    selected_answer: str


class SubmitQuizRequest(BaseModel):
    quiz_id: str
    answers: List[Answer]