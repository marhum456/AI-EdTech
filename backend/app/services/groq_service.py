from groq import Groq

from app.config import settings


class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

        # Default model
        self.model = "llama-3.3-70b-versatile"

    def generate_response(self, prompt: str) -> str:
        """
        Send a prompt to Groq and return the response.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1024,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Groq Error: {e}"


# Singleton instance
groq_service = GroqService()