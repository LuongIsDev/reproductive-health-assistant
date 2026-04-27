"""
main.py
───────
FastAPI server for the Reproductive Health Assistant.
Exposes a /chat endpoint that uses the CoordinatorAgent to route questions.
"""

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional

# ── Fix: Ensure local 'agents' folder is prioritized ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.agent_coordinator import CoordinatorAgent, AGENT_REGISTRY

# ── Setup FastAPI ──
app = FastAPI(
    title="Reproductive Health Assistant API",
    description="API for routing sexual health questions to specialized agents.",
    version="1.0.0"
)

# Initialize the coordinator once
coordinator = CoordinatorAgent()

# ── Pydantic Models ──
class Message(BaseModel):
    role: str      # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    agent_used: str
    question: str
    answer: str

# ── Endpoints ──

@app.get("/")
async def root():
    return {"message": "Reproductive Health Assistant API is running", "port": 8010}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handles a chat request. 
    Routes the message through the CoordinatorAgent with full history.
    """
    try:
        # Convert list of Pydantic models to list of dictionaries for the agent
        chat_history = [m.model_dump() for m in request.history] if request.history else []
        
        # Run the coordinator
        result = await coordinator.run(request.message, chat_history=chat_history)
        
        return result
        
    except Exception as e:
        import logging
        logging.error(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time streaming chat.
    """
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            user_message = data.get("message")
            chat_history = data.get("history", [])

            if not user_message:
                continue

            # 1. Routing phase (Fast, decide which agent to use)
            agent_name = await coordinator.get_route(user_message, chat_history=chat_history)
            
            # Send info about which agent was chosen (Frontend expects 'message')
            await websocket.send_json({"type": "info", "message": f"Routed to: {agent_name}"})

            # 2. Streaming phase
            agent = AGENT_REGISTRY.get(agent_name)
            if not agent:
                agent = AGENT_REGISTRY["general_health_agent"]

            full_answer = ""
            async for token in agent.run_stream(user_message, chat_history=chat_history):
                full_answer += token
                # Send each token to the client (Frontend expects 'content')
                await websocket.send_json({"type": "token", "content": token})

            # 3. Done phase (Frontend expects 'content')
            await websocket.send_json({"type": "done", "content": full_answer})

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
    except Exception as e:
        print(f"WebSocket Error: {e}")
        try:
            await websocket.send_json({"type": "error", "detail": str(e)})
        except:
            pass

# ── Entry Point ──
if __name__ == "__main__":
    # Run the server on port 9010
    print("\n🚀 Starting server at http://localhost:8010")
    print("📖 API Documentation: http://localhost:8010/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8010)
