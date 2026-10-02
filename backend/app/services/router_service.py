class RouterService:

    # -------------------------------------------------
    # Subject → Groq Model Route
    # -------------------------------------------------

    SUBJECT_ROUTES = {
        "computer_science": "openai/gpt-oss-20b",
        "mathematics": "openai/gpt-oss-120b",
        "physics": "openai/gpt-oss-120b",
        "chemistry": "openai/gpt-oss-120b",
    }

    # -------------------------------------------------
    # Route Subject
    # -------------------------------------------------

    def route_subject(self, subject: str) -> str:

        subject = subject.lower().strip()

        if subject not in self.SUBJECT_ROUTES:
            raise ValueError(
                f"Unsupported subject: {subject}. "
                f"Available subjects: "
                f"{list(self.SUBJECT_ROUTES.keys())}"
            )

        model_route = self.SUBJECT_ROUTES[subject]

        print(
            f"🔀 Router: {subject} → {model_route}"
        )

        return model_route


# Singleton instance

router_service = RouterService()