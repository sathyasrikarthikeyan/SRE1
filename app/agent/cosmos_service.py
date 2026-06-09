import os

from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

client = CosmosClient(
    os.getenv("COSMOS_ENDPOINT"),
    credential=os.getenv("COSMOS_KEY")
)

database = client.get_database_client(
    os.getenv("COSMOS_DATABASE")
)

container = database.get_container_client(
    os.getenv("COSMOS_CONTAINER")
)


def save_chat(chat_id, title, messages):

    item = {
        "id": chat_id,
        "chat_id": chat_id,
        "title": title,
        "messages": messages
    }

    container.upsert_item(item)


def get_chat(chat_id):

    try:
        item = container.read_item(
            item=chat_id,
            partition_key=chat_id
        )

        return item

    except Exception:
        return None


def get_all_chats():

    query = """
    SELECT *
    FROM c
    """

    items = list(
        container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
    )

    return items


def delete_chat(chat_id):

    container.delete_item(
        item=chat_id,
        partition_key=chat_id
    )