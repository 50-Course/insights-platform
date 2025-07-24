import os
from typing import Any

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_ai_insights(prompt: Any) -> str:
    """
    Generate AI insights using the DeepSeek Chimera model via OpenRouter API.

    This function sends a prompt to the model and returns the generated insights,
    which can be used to analyze data or provide recommendations but its stored locally
    at the moment as JSON.
    """
    # it would look at the rows of the file and generate insights based on the information
    # of the file, which is passed as a prompt.

    # if the text is a DataFrame, we convert it to a string representation
    if isinstance(prompt, str):
        # if the prompt is already a string, we use it as is
        pass
    # otherwise, we assume the prompt is a string
    elif hasattr(prompt, "to_string"):
        # if the prompt has a to_string method (like a DataFrame), we convert it to a string
        prompt = prompt.to_string(index=False)
    else:
        raise ValueError("Prompt must be a string or a DataFrame-like object.")

    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        extra_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Insights Generator",
        },
    )
    return response.choices[0].message.content
