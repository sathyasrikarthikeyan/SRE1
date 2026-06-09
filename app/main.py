from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent.chat_service import chat_with_agent
from app.agent.chat_store import chat_store
from app.agent.cosmos_service import save_chat

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

    chats = chat_store.get_chats()

    # Create chat if it doesn't exist
    if request.chat_id not in chats:

        chat_store.create_chat(
            request.chat_id,
            title="New Chat"
        )

        chats = chat_store.get_chats()

    # First user message becomes chat title
    if (
        request.chat_id in chats
        and chats[request.chat_id]["title"] == "New Chat"
    ):

        chat = chats[request.chat_id]

        chat["title"] = request.message[:40]

        save_chat(
            request.chat_id,
            chat["title"],
            chat["messages"]
        )

    # Save current user message
    chat_store.add_message(
        request.chat_id,
        "user",
        request.message
    )

    # Reload latest history from Cosmos DB
    history = chat_store.get_messages(
        request.chat_id
    )

    # Ask agent with full chat history
    response = await chat_with_agent(
        request.message,
        history
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