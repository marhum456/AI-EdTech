from datetime import datetime

import app.database.mongodb as mongodb


class ProgressRepository:

    def save_progress(
        self,
        quiz_id,
        subject,
        course,
        lesson,
        score,
        total_questions,
        percentage,
    ):

        document = {
            "quiz_id": quiz_id,
            "subject": subject,
            "course": course,
            "lesson": lesson,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "created_at": datetime.utcnow(),
        }

        result = mongodb.db.progress.insert_one(document)

        print(f"✅ Progress saved: {result.inserted_id}")

        return str(result.inserted_id)


progress_repository = ProgressRepository()