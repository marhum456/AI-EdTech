import json

from groq import Groq

from app.config import settings


class GroqService:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

        # Default model
        self.model = "llama-3.3-70b-versatile"

    def generate_response(self, prompt: str):
        """
        Send a prompt to Groq and return the response as JSON.
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
                temperature=0.2,
                max_tokens=2048,
            )

            content = response.choices[0].message.content

            # Remove markdown if Groq returns ```json ... ```
            content = content.strip()

            if content.startswith("```json"):
                content = content.replace("```json", "", 1)

            if content.startswith("```"):
                content = content.replace("```", "", 1)

            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

            # Convert JSON string into Python dictionary
            return json.loads(content)

        except json.JSONDecodeError:
            raise Exception(
                "Groq returned an invalid JSON response.\n\n"
                f"Response:\n{content}"
            )

        except Exception as e:
            raise Exception(f"Groq Error: {e}")


# Singleton instance
groq_service = GroqService()