from datetime import datetime
from bson import ObjectId

import app.database.mongodb as mongodb


class QuizRepository:

    def save_quiz(
        self,
        subject,
        course,
        lesson,
        number_of_questions,
        quiz,
    ):

        document = {
            "subject": subject,
            "course": course,
            "lesson": lesson,
            "number_of_questions": number_of_questions,
            "quiz": quiz["quiz"],
            "created_at": datetime.utcnow(),
        }

        result = mongodb.db.quizzes.insert_one(document)

        print(f"✅ Quiz saved with ID: {result.inserted_id}")

        return str(result.inserted_id)

    # -------------------------------------------------
    # Get Quiz by ID
    # -------------------------------------------------

    def get_quiz_by_id(self, quiz_id: str):

        quiz = mongodb.db.quizzes.find_one(
            {"_id": ObjectId(quiz_id)}
        )

        return quiz

    # -------------------------------------------------
    # Save Student Answers
    # -------------------------------------------------

    def save_student_answers(
        self,
        quiz_id: str,
        answers,
    ):

        mongodb.db.quizzes.update_one(
            {"_id": ObjectId(quiz_id)},
            {
                "$set": {
                    "student_answers": answers
                }
            }
        )


quiz_repository = QuizRepository()