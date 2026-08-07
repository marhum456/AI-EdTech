from pathlib import Path


class PromptService:

    def load_prompt(self, filename: str):

        prompt_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "prompts"
            / filename
        )

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()


prompt_service = PromptService()