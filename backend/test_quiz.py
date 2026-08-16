from app.services.quiz_service import quiz_service


quiz = quiz_service.generate_quiz(
    subject="web_developement",
    course="javascript_fundamentals",
    lesson="lesson_1",
    number_of_questions=5,
)

print("\n===== Generated Quiz =====\n")

print(quiz)

print("\n==========================\n")