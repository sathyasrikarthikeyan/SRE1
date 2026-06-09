from app.agent.cosmos_service import (
    save_chat,
    get_chat,
    get_all_chats
)


class ChatStore:

    def get_chats(self):

        chats = {}

        for item in get_all_chats():

            chats[item["chat_id"]] = {
                "title": item.get("title", "New Chat"),
                "messages": item.get("messages", [])
            }

        return chats

    def create_chat(self, chat_id, title="New Chat"):

        save_chat(
            chat_id,
            title,
            []
        )

    def add_message(self, chat_id, role, content):

        chat = get_chat(chat_id)

        if not chat:

            chat = {
                "chat_id": chat_id,
                "title": "New Chat",
                "messages": []
            }

        chat["messages"].append(
            {
                "role": role,
                "content": content
            }
        )

        save_chat(
            chat_id,
            chat["title"],
            chat["messages"]
        )

    def get_messages(self, chat_id):

        chat = get_chat(chat_id)

        if not chat:
            return []

        return chat["messages"]


chat_store = ChatStore()