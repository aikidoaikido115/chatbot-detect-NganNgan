from app.domain.interfaces import LineBotServiceInterface, LineMessagingInterface

class LineBotService(LineBotServiceInterface):
    def __init__(self, messaging_adapter: LineMessagingInterface):
        self.messaging_adapter = messaging_adapter  # Inject Dependency

    def handle_message(self, user_id: str, message: str) -> str:
        reply_text = f"Hello! How can I help you?\nuser_id:{user_id}\nmessage:{message}" # Business logic
        return reply_text
