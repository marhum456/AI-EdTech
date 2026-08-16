from app.services.create_subject_model_service import subject_model_service


# =================================================
# Test Prompts
# =================================================

tests = {
    "web_development": """
Create one simple multiple-choice question about JavaScript.

The question should be related to web development.
""",

    "mathematics": """
Create one simple multiple-choice question about mathematics.

The question should be related to basic algebra.
""",

    "physics": """
Create one simple multiple-choice question about physics.

The question should be related to basic motion.
"""
}


# =================================================
# Test Each Subject Model
# =================================================

for subject, prompt in tests.items():

    print("\n" + "=" * 60)
    print(f"Testing Subject: {subject}")
    print("=" * 60)

    try:

        result = subject_model_service.generate(
            subject=subject,
            prompt=prompt
        )

        print(result)

    except Exception as e:

        print(f"❌ Error testing {subject}:")
        print(e)