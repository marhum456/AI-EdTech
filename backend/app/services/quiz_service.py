from app.services.vector_service import vector_service
from app.services.prompt_service import prompt_service
from app.services.router_service import router_service
from app.services.create_subject_model_service import subject_model_service

from app.database.quiz_repository import quiz_repository
from app.database.progress_repository import progress_repository


class QuizService:

    # =================================================
    # Normalize Answer
    # =================================================

    def normalize_answer(self, answer: str) -> str:
        """
        Normalize answers before comparison.

        Handles:
        - Leading/trailing spaces
        - Upper/lower case differences
        - Normal spaces vs Unicode spaces
        """

        return (
            str(answer)
            .replace("\u00a0", " ")
            .replace("\u202f", " ")
            .strip()
            .lower()
        )

    # =================================================
    # Generate Quiz
    # =================================================

    def generate_quiz(
        self,
        subject: str,
        course: str,
        lesson: str,
        number_of_questions: int = 10,
    ):

        # =================================================
        # TEMPORARY DEBUG
        # =================================================

        print("\n===================================")
        print("QUIZ SERVICE RECEIVED:")
        print("subject =", repr(subject))
        print("course  =", repr(course))
        print("lesson  =", repr(lesson))
        print("===================================\n")

        # -------------------------------------------------
        # 1. Route Subject
        # -------------------------------------------------

        model_route = router_service.route_subject(subject)

        print(
            f"🤖 Selected route: {model_route}"
        )

        # -------------------------------------------------
        # 2. Retrieve Lesson Chunks from ChromaDB
        # -------------------------------------------------

        results = vector_service.get_lesson_chunks(
            subject=subject,
            course=course,
            lesson=lesson
        )

        documents = results["documents"]

        # TEMPORARY DEBUG
        print("\n===================================")
        print("CHROMADB RESULT:")
        print("Documents found =", len(documents))
        print("===================================\n")

        if not documents:
            raise Exception(
                f"No lesson content found for "
                f"{subject} / {course} / {lesson}"
            )

        context = "\n\n".join(documents)

        # -------------------------------------------------
        # 3. Load Prompt Template
        # -------------------------------------------------

        template = prompt_service.load_prompt(
            "quiz_prompt.txt"
        )

        prompt = template.format(
            context=context,
            number_of_questions=number_of_questions
        )

        # -------------------------------------------------
        # 4. Generate Quiz using Subject-Specific
        #    Groq Model
        # -------------------------------------------------

        quiz = subject_model_service.generate(
            subject=subject,
            prompt=prompt
        )

        # -------------------------------------------------
        # 5. Validate Quiz Response
        # -------------------------------------------------

        if not quiz or "quiz" not in quiz:

            raise Exception(
                "Invalid quiz response from subject model."
            )

        if not quiz["quiz"]:

            raise Exception(
                "Subject model returned an empty quiz."
            )

        # -------------------------------------------------
        # 6. Save Quiz to MongoDB
        # -------------------------------------------------

        quiz_id = quiz_repository.save_quiz(
            subject=subject,
            course=course,
            lesson=lesson,
            number_of_questions=number_of_questions,
            quiz=quiz
        )

        # -------------------------------------------------
        # 7. Return Quiz + Quiz ID + Route
        # -------------------------------------------------

        return {
            "quiz_id": quiz_id,
            "quiz": quiz["quiz"],
            "route": model_route
        }

    # =================================================
    # Submit Student Answers
    # =================================================

    def submit_quiz(
        self,
        quiz_id: str,
        answers,
    ):

        # -------------------------------------------------
        # 1. Retrieve Quiz
        # -------------------------------------------------

        quiz = quiz_repository.get_quiz_by_id(
            quiz_id
        )

        if not quiz:
            raise Exception(
                "Quiz not found."
            )

        # -------------------------------------------------
        # 2. Validate Answers
        # -------------------------------------------------

        if not answers:
            raise Exception(
                "No answers were submitted."
            )

        # -------------------------------------------------
        # 3. Save Student Answers
        # -------------------------------------------------

        quiz_repository.save_student_answers(
            quiz_id=quiz_id,
            answers=answers,
        )

        # -------------------------------------------------
        # 4. Calculate Score
        # -------------------------------------------------

        score = 0

        correct_answers = quiz["quiz"]

        for student_answer in answers:

            question_number = student_answer.get(
                "question"
            )

            if question_number is None:
                continue

            try:
                question_index = int(
                    question_number
                ) - 1

            except (ValueError, TypeError):
                continue

            if question_index < 0:
                continue

            if question_index >= len(correct_answers):
                continue

            selected_answer = student_answer.get(
                "selected_answer"
            )

            correct_answer = correct_answers[
                question_index
            ].get(
                "correct_answer"
            )

            if selected_answer is None:
                continue

            if correct_answer is None:
                continue

            normalized_student_answer = (
                self.normalize_answer(
                    selected_answer
                )
            )

            normalized_correct_answer = (
                self.normalize_answer(
                    correct_answer
                )
            )

            if (
                normalized_student_answer
                ==
                normalized_correct_answer
            ):

                score += 1

        # -------------------------------------------------
        # 5. Calculate Percentage
        # -------------------------------------------------

        total_questions = len(correct_answers)

        if total_questions == 0:

            percentage = 0

        else:

            percentage = round(
                (score / total_questions) * 100,
                2
            )

        # -------------------------------------------------
        # 6. Save Progress
        # -------------------------------------------------

        progress_id = progress_repository.save_progress(
            quiz_id=quiz_id,
            subject=quiz["subject"],
            course=quiz["course"],
            lesson=quiz["lesson"],
            score=score,
            total_questions=total_questions,
            percentage=percentage,
        )

        # -------------------------------------------------
        # 7. Return Result
        # -------------------------------------------------

        return {
            "message": "Quiz submitted successfully.",
            "progress_id": progress_id,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "student_answers": answers,
        }


# =================================================
# Singleton Instance
# =================================================

quiz_service = QuizService()