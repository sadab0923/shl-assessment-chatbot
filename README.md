# SHL Conversational Assessment Recommender

## Overview
This project is a conversational AI agent built for the SHL AI Intern assignment.

It helps recruiters and hiring managers discover relevant SHL assessments through natural language conversations.

## Features
- FastAPI backend
- Stateless conversation handling
- SHL-only recommendations
- Refusal handling for off-topic queries
- Recommendation refinement
- Swagger API docs

## API Endpoints

### GET /health
Returns service health.

Response:
{
  "status": "ok"
}

### POST /chat
Accepts conversation history and returns recommendations.

## Tech Stack
- FastAPI
- Gemini API
- Python
- GCP VM
- Swagger UI

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 5000
