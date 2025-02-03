from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import openai
import os
from dotenv import load_dotenv
import uuid
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and clean up resources"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        raise RuntimeError("Missing OpenAI API key")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    session_id: str | None = None

class Message(BaseModel):
    role: str
    content: str

class QueryResponse(BaseModel):
    response: str
    session_id: str
    history: List[Message]

# In-memory storage with TTL (basic example)
sessions: Dict[str, List[Message]] = {}

def get_session_history(session_id: str) -> List[Message]:
    """Retrieve or create session history"""
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        history = get_session_history(session_id)
        
        # Add user message to history
        user_message = Message(role="user", content=request.query)
        history.append(user_message)
        
        #  response
        try:
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[m.dict() for m in history],
                temperature=0.7,
                max_tokens=500
            )
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )
            
        ai_response = completion.choices[0].message['content']
        
        # Add assistant message to history
        assistant_message = Message(role="assistant", content=ai_response)
        history.append(assistant_message)
        
        # Keep only last 10 messages to manage memory
        if len(history) > 10:
            history = history[-10:]
            sessions[session_id] = history
            
        return QueryResponse(
            response=ai_response,
            session_id=session_id,
            history=history.copy()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )