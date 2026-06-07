import os
import asyncio

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient

load_dotenv()


async def main():

    print("Creating Foundry Client...")

    client = FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_NAME"),
        credential=DefaultAzureCredential()
    )

    print("Client Created Successfully")

    agent = client.as_agent(
        name="ServiceNowAgent",
        instructions="""
        You are a ServiceNow Operational Agent.

        Help users with:
        - Incident Management
        - Change Management
        - Service Requests
        - Knowledge Articles
        """
    )

    print("Agent Created Successfully")

    response = await agent.run(
        "What is ServiceNow?"
    )

    print("\nAgent Response:")
    print(response)


asyncio.run(main())