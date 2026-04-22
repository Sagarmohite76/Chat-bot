from google import genai
from app.core.config import setting

client = genai.Client(api_key=setting.Gemini_API_KEY)

def get_response(query, context):
    prompt = f"""
You are a helpful and intelligent chatbot assistant.
Please answer the user's question using the provided context.
If the context contains the answer, base your response on it, but use your own words to provide a conversational reply.
If the context is empty or doesn't contain the answer, just answer the question to the best of your ability.

Context:
{context}

Question:
{query}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
