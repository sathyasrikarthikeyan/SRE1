import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient

from app.agent.cosmos_service import get_all_chats

load_dotenv()

client = FoundryChatClient(
    project_endpoint=os.getenv("PROJECT_ENDPOINT"),
    model=os.getenv("MODEL_NAME"),
    credential=DefaultAzureCredential()
)

agent = client.as_agent(
    name="ServiceNowAgent",
    instructions="""
You are a ServiceNow Operational Agent.

Remember previous messages from the conversation.

Your responsibilities:
- Incident Management
- Change Management
- Service Requests
- Knowledge Articles

Provide concise, professional, and helpful responses.
"""
)


async def chat_with_agent(
    message: str,
    history: list
) -> str:

    # Current Chat History
    context = ""

    for item in history:
        context += (
            f"{item['role']}: "
            f"{item['content']}\n"
        )

    # Cross-Chat Memory
    all_chats = get_all_chats()[-5:]

    global_memory = ""

    for chat in all_chats:

        messages = chat.get("messages", [])[-5:]

        for msg in messages:

            global_memory += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

    prompt = f"""
You are a ServiceNow Operational Agent.

Known Information From Recent Chats:

{global_memory}

Current Chat History:

{context}

Current User Message:

{message}

Use:
1. Recent chat memory
2. Current chat history

when answering.
"""

    print("\n===== MEMORY SUMMARY =====")
    print(f"Loaded {len(all_chats)} recent chats")
    print("==========================\n")

    response = await agent.run(prompt)

    return str(response)