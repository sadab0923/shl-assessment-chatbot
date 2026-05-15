from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import google.generativeai as genai

# ---------------------------------------------------
# GEMINI CONFIG
# ---------------------------------------------------

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------

app = FastAPI()

# ---------------------------------------------------
# SHL CATALOG
# ---------------------------------------------------

SHL_CATALOG = [

    {
        "name": "Java 8 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "test_type": "K",
        "skills": [
            "java",
            "backend",
            "developer",
            "spring",
            "microservices"
        ]
    },

    {
        "name": "Python",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/python/",
        "test_type": "K",
        "skills": [
            "python",
            "backend",
            "engineer",
            "django",
            "flask"
        ]
    },

    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq32r/",
        "test_type": "P",
        "skills": [
            "personality",
            "leadership",
            "behavioral",
            "manager"
        ]
    },

    {
        "name": "Verify Interactive Numerical Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-interactive-numerical-reasoning/",
        "test_type": "A",
        "skills": [
            "analytical",
            "numerical",
            "reasoning",
            "data"
        ]
    },

    {
        "name": "Sales Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sales-solution/",
        "test_type": "S",
        "skills": [
            "sales",
            "business development",
            "client handling",
            "communication"
        ]
    }

]

# ---------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]

# ---------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "SHL Assessment Chatbot API is running"
    }

# ---------------------------------------------------
# HEALTH ENDPOINT
# ---------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    latest_message = request.messages[-1].content.lower()

    # ---------------------------------------------------
    # OFF-TOPIC REFUSAL
    # ---------------------------------------------------

    off_topic_keywords = [
        "weather",
        "movie",
        "cricket",
        "ipl",
        "bitcoin",
        "politics",
        "relationship",
        "legal advice",
        "football",
        "instagram"
    ]

    if any(word in latest_message for word in off_topic_keywords):

        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------------------------
    # VAGUE QUERY CLARIFICATION
    # ---------------------------------------------------

    if len(latest_message.split()) < 3:

        return {
            "reply": "Can you share the role, required skills, or seniority level you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------------------------
    # PERSONALITY TEST REFINEMENT
    # ---------------------------------------------------

    personality_required = (
        "personality" in latest_message
        or "leadership" in latest_message
        or "behavioral" in latest_message
    )

    recommendations = []

    # ---------------------------------------------------
    # RECOMMENDATION ENGINE
    # ---------------------------------------------------

    for item in SHL_CATALOG:

        matched = False

        for skill in item["skills"]:

            if skill.lower() in latest_message:
                matched = True

        if matched:

            recommendations.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"]
            })

    # ---------------------------------------------------
    # ADD PERSONALITY TESTS
    # ---------------------------------------------------

    if personality_required:

        for item in SHL_CATALOG:

            if item["test_type"] == "P":

                already_exists = any(
                    r["name"] == item["name"]
                    for r in recommendations
                )

                if not already_exists:

                    recommendations.append({
                        "name": item["name"],
                        "url": item["url"],
                        "test_type": item["test_type"]
                    })

    # ---------------------------------------------------
    # LIMIT MAX 10
    # ---------------------------------------------------

    recommendations = recommendations[:10]

    # ---------------------------------------------------
    # RETURN RECOMMENDATIONS
    # ---------------------------------------------------

    if recommendations:

        return {
            "reply": f"I found {len(recommendations)} SHL assessments matching your hiring requirements.",
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # ---------------------------------------------------
    # SAFE FALLBACK
    # ---------------------------------------------------

    return {
        "reply": "Please provide more details about the role, required skills, or assessment type.",
        "recommendations": [],
        "end_of_conversation": False
    }
