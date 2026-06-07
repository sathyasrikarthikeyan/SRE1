import os

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client(
    api_version=os.getenv("OPENAI_API_VERSION")
)


def chat_with_agent(message: str) -> str:

    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {
                "role": "system",
                "content": """
You are a ServiceNow Operational Agent.

Your responsibilities:
- Incident Management
- Change Management
- Service Requests
- Knowledge Articles

Provide concise, professional, and helpful responses.
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content