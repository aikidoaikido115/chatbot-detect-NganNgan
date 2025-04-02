from app.domain.interfaces import (
    LineBotServiceInterface,
    LineMessagingInterface,
    ImageStorageInterface,
    OcrInterface
)

class LineBotService(LineBotServiceInterface):
    def __init__(
        self, 
        messaging_adapter: LineMessagingInterface,
        image_storage: ImageStorageInterface,
        ocr:OcrInterface
    ):
        self.messaging_adapter = messaging_adapter  # Inject Dependency
        self.image_storage = image_storage
        self.ocr = ocr

    def handle_message(self, user_id: str, message: str) -> str:
        reply_text = f"สวัสดีครับ ส่งข้อความทำไม กรุณาส่งรูปเข้ามาได้เลย"
        # Business logic
        return reply_text
    
    def handle_image(self, user_id: str, image_id: str) -> str:
        image_content = self.messaging_adapter.get_image_content(image_id)
        self.image_storage.save_image(user_id, image_content)
        # OCR
        # print(image_content)
        reply_text = self.ocr.ocr(image_content)
        return reply_text
