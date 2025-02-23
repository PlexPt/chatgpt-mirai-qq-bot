from revChatGPT.revChatGPT import Chatbot, generate_uuid
import json
with open("config.json", "r") as jsonfile:
    config_data = json.load(jsonfile)

# Refer to https://github.com/acheong08/ChatGPT
bot = Chatbot(config_data["openai"], conversation_id=None, base_url=config_data["base_url"] if "base_url" in config_data else "https://chat.openai.com/")
class ChatSession:
    def __init__(self):
        self.reset_conversation()
    def reset_conversation(self):
        self.conversation_id = None
        self.parent_id = generate_uuid()
        self.prev_conversation_id = None
        self.prev_parent_id = None
    def rollback_conversation(self) -> bool:
        if self.prev_parent_id is not None:
            self.conversation_id = self.prev_conversation_id
            self.parent_id = self.prev_parent_id
            self.prev_conversation_id = None
            self.prev_parent_id = None
            return True
        else:
            return False
    def get_chat_response(self, message, output="text"):
        try:
            self.prev_conversation_id = self.conversation_id
            self.prev_parent_id = self.parent_id
            return bot.get_chat_response(message, output=output, conversation_id=self.conversation_id, parent_id=self.parent_id)
        finally:
            self.conversation_id = bot.conversation_id
            self.parent_id = bot.parent_id
sessions = {}


def get_chat_session(id: str):
    if id not in sessions:
        sessions[id] = ChatSession()
    return sessions[id]