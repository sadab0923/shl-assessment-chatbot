from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI()


# Sample SHL catalog
catalog = [
    {
        "name": "Java 8 (New)",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "test_type": "K",
        "skills": ["java", "spring", "backend", "developer"]
    },
    {
        "name": "Python",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/python/",
        "test_type": "K",
        "skills": ["python", "django", "flask", "backend"]
    },
    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq32r/",
        "test_type": "P",
        "skills": ["personality", "leadership", "behavioral"]
    },
    {
        "name": "Verify Interactive Numerical Reasoning",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/verify-interactive-numerical-reasoning/",
        "test_type": "A",
        "skills": ["numerical", "analytical", "reasoning"]
    },
    {
        "name": "Sales Solution",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/sales-solution/",
        "test_type": "S",
        "skills": ["sales", "communication", "client"]
    }
]


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/")
def home():
    return {
        "message": "SHL Assessment Chatbot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


def is_off_topic(query):

    blocked_topics = [
        "weather",
        "movie",
        "cricket",
        "ipl",
        "bitcoin",
        "politics",
        "instagram",
        "football"
    ]

    for word in blocked_topics:
        if word in query:
            return True

    return False


def needs_clarification(query):

    if len(query.split()) < 3:
        return True

    vague_queries = [
        "assessment",
        "test",
        "job",
        "hiring"
    ]

    return query in vague_queries


def find_recommendations(query):

    results = []

    for item in catalog:

        matched = False

        for skill in item["skills"]:

            if skill in query:
                matched = True
                break

        if matched:

            results.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"]
            })

    # add personality test if requested
    if "personality" in query or "leadership" in query:

        for item in catalog:

            if item["test_type"] == "P":

                already_added = any(
                    r["name"] == item["name"]
                    for r in results
                )

                if not already_added:

                    results.append({
                        "name": item["name"],
                        "url": item["url"],
                        "test_type": item["test_type"]
                    })

    return results[:10]


@app.post("/chat")
def chat(request: ChatRequest):

    query = request.messages[-1].content.lower()

    # refuse off-topic questions
    if is_off_topic(query):

        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ask follow-up for vague queries
    if needs_clarification(query):

        return {
            "reply": "Can you share the role, skills, or experience level you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = find_recommendations(query)

    # return recommendations
    if recommendations:

        return {
            "reply": f"I found {len(recommendations)} SHL assessments matching your requirement.",
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # fallback response
    return {
        "reply": "I could not find a matching SHL assessment. Please provide more details.",
        "recommendations": [],
        "end_of_conversation": False
    }
