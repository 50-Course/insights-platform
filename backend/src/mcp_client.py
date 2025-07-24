import json
import os
import re
from typing import Any

from fastapi.logger import logger
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_ai_insights(prompt: Any):
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

    full_prompt = f"""
    Analyze the following data and return 3 insights in strict JSON format.

    Each insight must contain:
    - title (str)
    - description (str)
    - confidence_score (float)
    - reference_rows (list[int])

    Respond ONLY with raw JSON.

    Data:
    {prompt}
    """
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        extra_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Insights Generator",
        },
    )
    raw_response = response.choices[0].message.content
    logger.debug(f"AI Response: \n{response}")

    # now that we got back something like:
    #
    # blablabla
    #
    # ###
    #
    # [
    #   {
    #   i      jadjgakt...
    #   }
    #
    # ]

    # if we encounter code blockers, stript those out first
    try:
        # Handle code block markdown: ```json ... ```
        match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw_response, re.DOTALL)
        json_str = match.group(1) if match else raw_response.strip()

        # then clean-up: strip stray characters before `[` or after `]`
        json_str = json_str.strip()
        json_str = re.sub(r"^[^\[]*", "", json_str)  # left trim garbage before first [
        json_str = re.sub(r"[^\]]*$", "", json_str)  # right trim garbage after last ]

        insights = json.loads(json_str)
        return insights

    except json.JSONDecodeError as e:
        logger.error(f"[ERROR] Failed to decode JSON from LLM: {e}")
        raise ValueError("Failed to parse AI response as JSON.")
