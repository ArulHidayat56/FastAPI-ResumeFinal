import asyncio
from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

async def call_groq_api(prompt: str):
    return await asyncio.to_thread(
        client.chat.completions.create,
        messages=[{"role": "user", "content": prompt}],
        model=MODEL_NAME,
        temperature=0.2
    )
