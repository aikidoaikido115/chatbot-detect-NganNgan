from abc import ABC, abstractmethod

class LineBotServiceInterface(ABC):
    @abstractmethod
    def handle_message(self, user_id: str, message: str) -> str:
        pass


class LineMessagingInterface(ABC):
    @abstractmethod
    def send_message(self, reply_token: str, message: str):
        pass




# class สำหรับ flex