"""
utils.py

This module provides functionalities to prepare data for a Large Language Model (LLM)
prompt based on user (member) profile and transaction history, and to retrieve
recommendations from the LLM. It uses Jinja2 templating for prompt generation,
pydantic models for structured output, and the OpenAI API for LLM requests.
"""

import json
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI

# Load environment variables from a .env file (e.g., OPENAI_API_KEY).
load_dotenv()

# Instantiate OpenAI client with the provided API key.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


with open("data/data.json", "r") as f:
    data = json.load(f)

# Create a lookup dictionary for members by their IDs.
members = {m["member_id"]: m for m in data["members"]}

# Create a lookup dictionary for experiences by their IDs.
experiences = {e["experience_id"]: e for e in data["experiences"]}


def data_preparation(member_id: str) -> str:
    """
    Creates a prompt for the LLM based on a given member's profile and transaction data.

    The function gathers:
    - The member's basic info (name, location).
    - The member's past redeemed offers and categorizes them.
    - The available experiences that the member has not redeemed yet.
    - The member's card transactions (merchant, category, and amount).
    These details are then rendered into a Jinja2 template to form a structured prompt.

    Args:
        member_id (str): The unique identifier of the member.

    Returns:
        str: The generated prompt string for the LLM. If the member does not exist,
        returns None.
    """
    member = members.get(member_id)
    if not member:
        return None

    # Identify past redeemed experiences for the member.
    past_experiences = {
        e["experience_id"]: {
            "title": experiences[e["experience_id"]]["title"],
            "category": experiences[e["experience_id"]].get("category", "Unknown"),
        }
        for e in member.get("past_redeemed_offers", [])
        if e["experience_id"] in experiences
    }

    # Identify experiences not yet redeemed by the member.
    available_experiences = [
        {
            "title": e["title"],
            "category": e.get("category", "Unknown"),
        }
        for e in experiences.values()
        if e["experience_id"] not in past_experiences
    ]

    # Gather the member's transaction data.
    transactions = [
        {
            "merchant": t["merchant_name"],
            "category": t["category"],
            "amount": f"£{t['amount']}",
        }
        for t in member.get("card_transactions", [])
    ]

    # Load Jinja2 template (prompt.jinja2 should be located in the same directory).
    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("prompt.jinja2")

    # Render template with dynamic values.
    prompt = template.render(
        name=member["name"],
        location=member["location"],
        past_experiences=past_experiences.values(),
        available_experiences=available_experiences,
        transactions=transactions,
    )

    return prompt
