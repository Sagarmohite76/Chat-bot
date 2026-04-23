from google import genai
from app.core.config import setting

client = genai.Client(api_key=setting.Gemini_API_KEY)

def get_response(query, context):
    prompt = f"""
Use ONLY the provided context.
If answer not found, say "I don't know".

Context:
{context}

Question:
{query}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    usage = response.usage_metadata
    print(f"""
    📊 Gemini Usage Breakdown:
    Prompt Tokens   : {usage.prompt_token_count}
    Thought Tokens  : {usage.thoughts_token_count}
    Output Tokens   : {usage.candidates_token_count}
    Total Tokens    : {usage.total_token_count}
    """)
    return response.text
