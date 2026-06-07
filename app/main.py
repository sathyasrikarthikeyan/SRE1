from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent.chat_service import chat_with_agent
from app.agent.chat_store import chat_store

app = FastAPI()


class ChatRequest(BaseModel):
    chat_id: str
    message: str


@app.get("/")
async def home():
    return FileResponse("app/static/index.html")


@app.post("/new-chat")
async def new_chat():

    chat_id = str(uuid4())

    chat_store.create_chat(
        chat_id,
        title="New Chat"
    )

    return {
        "chat_id": chat_id
    }


@app.get("/chats")
async def get_chats():

    return chat_store.get_chats()


@app.get("/chat/{chat_id}")
async def get_chat(chat_id: str):

    return {
        "messages": chat_store.get_messages(chat_id)
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    # Create chat if not exists
    if request.chat_id not in chat_store.chats:
        chat_store.create_chat(request.chat_id)

    # First user message becomes title
    if (
        chat_store.chats[request.chat_id]["title"]
        == "New Chat"
    ):
        chat_store.chats[request.chat_id]["title"] = (
            request.message[:40]
        )

    # Save user message
    chat_store.add_message(
        request.chat_id,
        "user",
        request.message
    )

    # Get AI response
    response = await chat_with_agent(
        request.message
    )

    # Save assistant response
    chat_store.add_message(
        request.chat_id,
        "assistant",
        response
    )

    return {
        "response": response
    }