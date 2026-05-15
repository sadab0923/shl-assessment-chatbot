from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

# Gemini API Key
genai.configure(api_key="AIzaSyAV9I-KE3oXAYJuFprUSWDRD1k9F-wPqmI")

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# -----------------------------
# SHL Catalog (Sample)
# -----------------------------
SHL_CATALOG = [
    {
        "name": "Java 8 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "test_type": "K",
        "skills": ["java", "backend", "developer"]
    },
    {
        "name": "Python",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/python/",
        "test_type": "K",
        "skills": ["python", "backend", "developer"]
    },
    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq32r/",
        "test_type": "P",
        "skills": ["personality", "leadership", "behavior"]
    },
    {
        "name": "Verify Interactive - Numerical Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-interactive-numerical-reasoning/",
        "test_type": "A",
        "skills": ["analytical", "numerical", "reasoning"]
    }
]

# -----------------------------
# Request Models
# -----------------------------
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    latest_message = request.messages[-1].content.lower()

    # -----------------------------
    # Refusal Handling
    # -----------------------------
    off_topic = [
        "weather",
        "movie",
        "politics",
        "legal",
        "cricket"
    ]

    if any(word in latest_message for word in off_topic):
        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Clarification
    # -----------------------------
    vague_queries = [
        "assessment",
        "test",
        "hiring",
        "job"
    ]

    if len(latest_message.split()) < 3:
        return {
            "reply": "Can you share the role or skills you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Recommendation Logic
    # -----------------------------
    recommendations = []

    for item in SHL_CATALOG:
        for skill in item["skills"]:
            if skill in latest_message:
                recommendations.append({
                    "name": item["name"],
                    "url": item["url"],
                    "test_type": item["test_type"]
                })
                break

    # max 10
    recommendations = recommendations[:10]

    # -----------------------------
    # If recommendations found
    # -----------------------------
    if recommendations:
        return {
            "reply": f"I found {len(recommendations)} SHL assessments for your requirement.",
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # -----------------------------
    # Gemini fallback
    # -----------------------------
    prompt = f"""
    User hiring requirement:
    {latest_message}

    Suggest relevant assessment areas only.
    """

    response = model.generate_content(prompt)

    return {
        "reply": response.text,
        "recommendations": [],
        "end_of_conversation": False
    }
