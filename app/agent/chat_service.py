import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient

from app.agent.memory import memory_service

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


async def chat_with_agent(message: str) -> str:

    # Save user message
    memory_service.save_message(
        "user",
        message
    )

    # Build conversation history
    context = ""

    for item in memory_service.get_history():
        context += f"{item['role']}: {item['content']}\n"

    prompt = f"""
Conversation History:

{context}

Current User Message:
{message}
"""

    # Call agent
    response = await agent.run(prompt)

    answer = str(response)

    # Save assistant response
    memory_service.save_message(
        "assistant",
        answer
    )

    return answer