"""
utils.py

This module provides functionalities to prepare data for a Large Language Model (LLM)
prompt based on user (member) profile and transaction history, and to retrieve
recommendations from the LLM. It uses Jinja2 templating for prompt generation,
pydantic models for structured output, and the OpenAI API for LLM requests.
"""

import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from src.data_classes import Recommendations
from src.data_preparation import data_preparation

# Load environment variables from a .env file (e.g., OPENAI_API_KEY).
load_dotenv()

# Instantiate OpenAI client with the provided API key.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_recommendations(member_id: str) -> dict:
    """
    Generates recommendations by calling the LLM with a dynamically created prompt.

    1. Calls `data_preparation` to generate the prompt.
    2. Sends the prompt to the LLM (OpenAI client) and expects structured JSON back.
    3. Parses the JSON response into pydantic models (Recommendations).

    Args:
        member_id (str): The unique identifier of the member.

    Returns:
        dict: A dictionary containing:
            - "member_id": the provided member_id.
            - "recommendations": a list of Recommendation objects,
              or an error message if the member_id is not found.
    """
    prompt = data_preparation(member_id)
    if not prompt:
        return {"error": "Member not found"}

    # Call a Beta endpoint of the OpenAI API (this is a placeholder model name).
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",  # Replace with an actual OpenAI-compatible model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        response_format=Recommendations,
    )

    # The parsed response contains a list of recommendations in .choices[0].message.parsed.
    recommendations = completion.choices[0].message.parsed

    return {"member_id": member_id, "recommendations": recommendations.recommendations}
