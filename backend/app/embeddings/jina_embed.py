import httpx
from app.core.config import setting

def get_embedding(text):
    url = setting.JINA_EMBED_URL

    headers = {
        "Authorization": f"Bearer {setting.JINA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": text,
        "model": "jina-embeddings-v2-base-en"
    }

    with httpx.Client(timeout=30.0) as client:  
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
    
# print(get_embedding("hello"))

# Testing purpose
# import asyncio

# async def main():
#     result = await get_embedding("hello")
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())