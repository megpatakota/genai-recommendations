import json
import openai
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import re
from typing import List, Dict, Any
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Recommendation(BaseModel):
    title: str
    category: str
    explanation: str


class Recommendations(BaseModel):
    recommendations: List[Recommendation]


# Load synthetic dataset
with open("data.json", "r") as f:
    data = json.load(f)

members = {m["member_id"]: m for m in data["members"]}
experiences = {e["experience_id"]: e for e in data["experiences"]}

# Prepare data for the LLM
def data_preparation(member_id):
    """Creates a prompt for the LLM based on user profile & transaction data."""
    member = members.get(member_id)
    if not member:
        return None

    past_experiences = {
        e["experience_id"]: {
            "title": experiences[e["experience_id"]]["title"],
            "category": experiences[e["experience_id"]].get("category", "Unknown"),
        }
        for e in member.get("past_redeemed_offers", [])
        if e["experience_id"] in experiences
    }

    available_experiences = [
        {
            "title": e["title"],
            "category": e.get("category", "Unknown"),
        }
        for e in experiences.values()
        if e["experience_id"] not in past_experiences
    ]

    transactions = [
        {
            "merchant": t["merchant_name"],
            "category": t["category"],
            "amount": f"£{t['amount']}",
        }
        for t in member.get("card_transactions", [])
    ]

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("prompt.jinja2")

    # Render template with dynamic values
    prompt = template.render(
        name=member["name"],
        location=member["location"],
        past_experiences=past_experiences.values(),
        available_experiences=available_experiences,
        transactions=transactions,
    )

    print(prompt)

    return prompt


def get_recommendations(member_id):
    """Calls the LLM with the generated prompt and returns recommendations."""
    prompt = data_preparation(member_id)
    if not prompt:
        return {"error": "Member not found"}

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",  # Replace with OpenAI-compatible model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        response_format=Recommendations,
    )

    recommendations = completion.choices[0].message.parsed

    return {"member_id": member_id, "recommendations": recommendations.recommendations}
