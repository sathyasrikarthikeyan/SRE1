import os

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=AzureCliCredential()
)

print("Connected Successfully!")