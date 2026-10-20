import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from pipeline import run_research_pipeline

# Load environment variables from the project folder
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(
    title="ResearchMind API",
    description="Multi-Agent AI Research API",
    version="1.0.0"
)

MY_API_KEY = os.getenv("MY_API_KEY")


class ResearchRequest(BaseModel):
    topic: str = Field(
        min_length=1,
        max_length=500,
        description="Topic to research"
    )


@app.get("/")
def home():
    return {
        "message": "ResearchMind API is running",
        "docs": "/docs"
    }


@app.post("/research")
def research(
    request: ResearchRequest,
    x_api_key: str = Header(default="")
):
    # Authenticate the caller
    if not MY_API_KEY or x_api_key != MY_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    topic = request.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Research topic cannot be empty"
        )

    try:
        # Run your existing four-agent pipeline
        result = run_research_pipeline(topic)

        return {
            "success": True,
            "topic": topic,
            "search_results": result["search_results"],
            "scraped_content": result["scraped_content"],
            "report": result["report"],
            "feedback": result["feedback"]
        }

    except Exception:
        # Avoid exposing internal errors or credentials
        raise HTTPException(
            status_code=500,
            detail=(
                "Research failed. Check the API server terminal "
                "for the underlying error."
            )
        )