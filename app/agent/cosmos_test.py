from cosmos_service import (
    save_chat,
    get_chat,
    get_all_chats
)

save_chat(
    "chat1",
    "First Cosmos Chat",
    [
        {
            "role": "user",
            "content": "Hello Cosmos"
        }
    ]
)

print("Saved")

chat = get_chat("chat1")

print(chat)

print("All Chats")

print(get_all_chats())