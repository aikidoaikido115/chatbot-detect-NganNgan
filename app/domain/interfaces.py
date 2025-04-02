from abc import ABC, abstractmethod


class ImageStorageInterface(ABC):
    @abstractmethod
    def save_image(self, user_id: str, image_content: bytes) -> str:
        pass

class OcrInterface(ABC):
    @abstractmethod
    def ocr(self, image_content: bytes) -> str:
        pass

class LineBotServiceInterface(ABC):
    @abstractmethod
    def handle_message(self, user_id: str, message: str) -> str:
        pass

    @abstractmethod
    def handle_image(self, user_id: str, image_id: str) -> str:
        pass


class LineMessagingInterface(ABC):
    @abstractmethod
    def send_message(self, reply_token: str, message: str):
        pass
    @abstractmethod
    def get_image_content(self, message_id: str) -> bytes:
        pass




# class สำหรับ flex