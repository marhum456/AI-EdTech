from app.services.vector_service import vector_service
from app.services.groq_service import groq_service


class QuizService:

    def generate_quiz(
        self,
        subject: str,
        course: str,
        lesson: str,
        number_of_questions: int = 10,
    ):

        # -------------------------------------------------
        # 1. Retrieve all lesson chunks
        # -------------------------------------------------

        results = vector_service.get_lesson_chunks(
            subject=subject,
            course=course,
            lesson=lesson
        )

        documents = results["documents"]

        context = "\n\n".join(documents)

        # -------------------------------------------------
        # 2. Build Prompt
        # -------------------------------------------------

        prompt = f"""
You are an expert university quiz generator.

You must generate the quiz ONLY from the lesson content below.

Do NOT use your own knowledge.
Do NOT invent information.
If the lesson does not contain enough information,
generate questions only from what is provided.

Lesson Content:

{context}

Generate {number_of_questions} multiple-choice questions.

Rules:
- Every question must have four options.
- Only one option should be correct.
- Cover different topics from the lesson.
- Avoid repeating questions.
- Use clear and simple language.

Return ONLY the quiz.
"""

        # -------------------------------------------------
        # 3. Generate Quiz
        # -------------------------------------------------

        quiz = groq_service.generate_response(prompt)

        return quiz

        print(quiz)

quiz_service = QuizService()
