from abc import ABC, abstractmethod

class ImageStorageInterface(ABC):
    @abstractmethod
    def save_image(self, user_id: str, image_content: bytes) -> str:
        pass

class OcrInterface(ABC):
    @abstractmethod
    def ocr(self, image_content: bytes) -> str:
        pass

class ImageEnhanceInterface(ABC):
    @abstractmethod
    def apply_conv_sharpen(self, image_content: bytes) -> bytes:
        pass

    @abstractmethod
    def apply_unsharp_mask(self, image_content: bytes, sigma: float, strength: float) -> bytes:
        pass

    @abstractmethod
    def apply_laplacian_sharpen(self, image_content: bytes, alpha: float) -> bytes:
        pass

    @abstractmethod
    def apply_gaussian_subtract(self, image_content: bytes, ksize: int) -> bytes:
        pass

class LineBotServiceInterface(ABC):
    @abstractmethod
    def handle_message(self, user_id: str, message: str) -> object:
        pass

    @abstractmethod
    def handle_image(self, user_id: str, image_id: str) -> object:
        pass


class LineMessagingInterface(ABC):
    @abstractmethod
    def send_message(self, reply_token: str, message: str):
        pass
    
    @abstractmethod
    def send_flex(self, reply_token: str, flex_message: dict):
        pass

    @abstractmethod
    def get_image_content(self, message_id: str) -> bytes:
        pass