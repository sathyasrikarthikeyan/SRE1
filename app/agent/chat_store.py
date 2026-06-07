class ChatStore:

    def __init__(self):
        self.chats = {}

    def create_chat(self, chat_id, title="New Chat"):

        self.chats[chat_id] = {
            "title": title,
            "messages": []
        }

    def get_chats(self):

        return self.chats

    def get_chat(self, chat_id):

        if chat_id not in self.chats:
            return None

        return self.chats[chat_id]

    def add_message(self, chat_id, role, content):

        if chat_id not in self.chats:
            self.create_chat(chat_id)

        self.chats[chat_id]["messages"].append(
            {
                "role": role,
                "content": content
            }
        )

    def get_messages(self, chat_id):

        if chat_id not in self.chats:
            return []

        return self.chats[chat_id]["messages"]

    def update_title(self, chat_id, title):

        if chat_id not in self.chats:
            return

        self.chats[chat_id]["title"] = title

    def delete_chat(self, chat_id):

        if chat_id in self.chats:
            del self.chats[chat_id]


chat_store = ChatStore()