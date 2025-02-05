from pydantic import BaseModel
from typing import List


class Recommendation(BaseModel):
    """
    Represents an individual recommendation from the LLM.

    Attributes:
        title (str): The title or name of the recommended item.
        category (str): The category or type of the recommendation.
        explanation (str): A textual explanation or justification for the recommendation.
    """

    title: str
    category: str
    explanation: str


class Recommendations(BaseModel):
    """
    A collection of Recommendation objects.

    Attributes:
        recommendations (List[Recommendation]): A list of Recommendation items.
    """

    recommendations: List[Recommendation]


class RecommendationsResponse(BaseModel):
    member_id: str
    recommendations: List[Recommendation]
