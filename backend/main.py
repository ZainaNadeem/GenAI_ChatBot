"""
BCG GenAI Financial Chatbot — FastAPI Backend
Exposes chatbot logic as a REST API.
React frontend communicates with this server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot_engine import build_response

# APP SETUP
app = FastAPI(
    title="BCG GenAI Financial Chatbot API",
    description="Natural language queries on SEC 10-K financial data",
    version="1.0.0"
)

# CORS MIDDLEWARE
# Allows React (running on port 3000) to talk to FastAPI (port 8000)
# Without this the browser blocks cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REQUEST/RESPONSE MODELS
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    is_exit: bool = False

# ENDPOINTS
@app.get("/")
def health_check():
    """Confirm the API is running."""
    return {
        "status": "online",
        "message": "BCG GenAI Financial Chatbot API is running"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Receive a user message and return a chatbot response.
    """
    response = build_response(request.message)
    is_exit = response == "exit"

    if is_exit:
        response = "Goodbye! Happy to help with financial analysis anytime."

    return ChatResponse(response=response, is_exit=is_exit)