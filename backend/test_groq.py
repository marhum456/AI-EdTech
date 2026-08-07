from app.services.groq_service import groq_service

prompt = """
Explain JavaScript variables in simple words.
"""

response = groq_service.generate_response(prompt)

print("\n===== Groq Response =====\n")
print(response)
print("\n=========================\n")