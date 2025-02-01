from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from utils import get_recommendations
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Yonder Experience Recommender API",
    description="Provides personalised Yonder Experience recommendations based on member data.",
    version="1.0.0"
)

# Pydantic model for structured recommendation data
class Recommendation(BaseModel):
    title: str
    category: str
    explanation: str

class RecommendationsResponse(BaseModel):
    member_id: str
    recommendations: List[Recommendation]

@app.get("/recommendations/{member_id}", response_model=RecommendationsResponse)
async def recommendations_endpoint(member_id: str, output: str = Query("json", enum=["json", "text"])):
    """
    Get personalised recommendations for a member.
    
    Query parameter 'output':
    - 'json' returns a structured list of recommendations (default).
    - 'text' returns a generated text block explaining why each experience might suit the member.
    """
    result = get_recommendations(member_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    if output == "json":
        # Return the structured JSON response
        return result
    else:
        # Build a text block response
        text_response = f"Personalised Recommendations for Member {member_id}:\n\n"
        # Loop over each recommendation and append details to the text block.
        for rec in result["recommendations"]:
            # If using pydantic objects, you can access the attributes directly:
            text_response += f"Experience Title: {rec.title}\n"
            text_response += f"Category: {rec.category}\n"
            text_response += f"Why it's recommended: {rec.explanation}\n\n"
        return PlainTextResponse(text_response)

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

# Optionally add a root endpoint with a friendly message
@app.get("/")
async def root():
    return {"message": "Welcome to the Yonder Experience Recommender API. Please visit /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
