import os

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_insights(prompt: str) -> str:
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        extra_headers={
            "HTTP-Referer": "http://localhost:8000",  # optional
            "X-Title": "AI Insights FastAPI Demo",  # optional
        },
    )
    return response.choices[0].message.content
