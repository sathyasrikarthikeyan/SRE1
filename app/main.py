from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent.chat_service import chat_with_agent

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.post("/chat")
def chat(request: ChatRequest):

    response = chat_with_agent(request.message)

    return {
        "response": response
    }