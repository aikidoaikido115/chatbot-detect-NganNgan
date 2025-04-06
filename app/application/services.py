from app.domain.interfaces import (
    LineBotServiceInterface,
    LineMessagingInterface,
    ImageStorageInterface,
    OcrInterface,
    ImageEnhanceInterface
)

class LineBotService(LineBotServiceInterface):
    def __init__(
        self, 
        messaging_adapter: LineMessagingInterface,
        image_storage: ImageStorageInterface,
        ocr:OcrInterface,
        enhance:ImageEnhanceInterface
    ):
        self.messaging_adapter = messaging_adapter  # Inject Dependency
        self.image_storage = image_storage
        self.ocr = ocr
        self.enhance = enhance

    def handle_message(self, user_id: str, message: str) -> str:
        reply_text = f"สวัสดีครับ ส่งข้อความทำไม กรุณาส่งรูปเข้ามาได้เลย\nลองพิมพ์คำว่า 'flex' ดูสิ"
        # Business logic สำหรับ Rich menu
        if message == "flex":
            reply_text = "ส่ง flex ให้แล้วนะครับ"
        return reply_text
    
    def handle_image(self, user_id: str, image_id: str) -> str:
        image_content = self.messaging_adapter.get_image_content(image_id)
        self.image_storage.save_image(user_id, image_content)
        # OCR
        # print(image_content)
        image_content = self.enhance.apply_sharpen(image_content)
        reply_text = self.ocr.ocr(image_content)
        return reply_text
