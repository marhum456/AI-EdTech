import json

from groq import Groq

from app.config import settings


class SubjectModelService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        # -------------------------------------------------
        # Subject-specific Groq models
        # -------------------------------------------------

        self.models = {
            "web_developement": "openai/gpt-oss-20b",
            "mathematics": "openai/gpt-oss-120b",
            "physics": "openai/gpt-oss-120b",
        }

    # -------------------------------------------------
    # Structured Quiz Schema
    # -------------------------------------------------

    QUIZ_SCHEMA = {
        "type": "object",
        "properties": {
            "quiz": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string"
                        },
                        "options": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "correct_answer": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "question",
                        "options",
                        "correct_answer"
                    ],
                    "additionalProperties": False
                }
            }
        },
        "required": [
            "quiz"
        ],
        "additionalProperties": False
    }

    # -------------------------------------------------
    # Generate Quiz
    # -------------------------------------------------

    def generate(
        self,
        subject: str,
        prompt: str
    ):

        subject = subject.lower().strip()

        # -------------------------------------------------
        # Check Subject
        # -------------------------------------------------

        if subject not in self.models:
            raise ValueError(
                f"No model configured for subject: {subject}. "
                f"Available subjects: {list(self.models.keys())}"
            )

        # -------------------------------------------------
        # Select Model
        # -------------------------------------------------

        model = self.models[subject]

        print(
            f"🤖 Subject Model: {subject} → {model}"
        )

        # -------------------------------------------------
        # Call Groq with Structured Output
        # -------------------------------------------------

        response = self.client.chat.completions.create(
            model=model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a specialized educational quiz "
                        "generator. Use ONLY the provided lesson "
                        "content. Generate multiple-choice questions "
                        "and return the requested JSON structure."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "quiz",
                    "strict": True,
                    "schema": self.QUIZ_SCHEMA
                }
            },

            temperature=0.3,
            max_tokens=2048,
        )

        # -------------------------------------------------
        # Get Response
        # -------------------------------------------------

        content = response.choices[0].message.content

        if not content:
            raise Exception(
                "Groq returned an empty response."
            )

        # -------------------------------------------------
        # Convert JSON → Python Dictionary
        # -------------------------------------------------

        try:

            quiz = json.loads(content)

        except json.JSONDecodeError as e:

            raise Exception(
                f"Failed to parse Groq JSON response: {e}"
            )

        # -------------------------------------------------
        # Final Validation
        # -------------------------------------------------

        if "quiz" not in quiz:
            raise Exception(
                "Invalid quiz response: 'quiz' field missing."
            )

        return quiz


# -------------------------------------------------
# Singleton Instance
# -------------------------------------------------

subject_model_service = SubjectModelService()