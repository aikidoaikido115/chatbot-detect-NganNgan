from fastapi import APIRouter, Depends
from app.application.services import LineBotService
from app.domain.interfaces import LineBotServiceInterface
from app.domain.models import LineWebhookRequest, LineMessageEvent
from app.infrastructure.line_api import LineMessagingAdapter
from app.infrastructure.file_storage import ImageStorageAdapter
from app.infrastructure.ocr_api import OcrAdapter
from app.infrastructure.image_enhance import ImageEnhanceAdapter

router = APIRouter()

def get_line_bot_service() -> LineBotServiceInterface:
    messaging_adapter = LineMessagingAdapter()
    image_storage = ImageStorageAdapter()
    ocr = OcrAdapter()
    enhance = ImageEnhanceAdapter()
    return LineBotService(messaging_adapter, image_storage, ocr, enhance)

@router.get("/")
async def hello():
    return {"message":"Welcome to Chatbot"}
@router.post("/webhook")
async def line_webhook(
    webhook: LineWebhookRequest,
    bot_service: LineBotServiceInterface = Depends(get_line_bot_service)
):
    results = []
    for event in webhook.events:
        message_event = LineMessageEvent.from_webhook_event(event)

        if not message_event:
            results.append({"event_id": event.webhookEventId, "processed": False})
            continue

        if message_event.message_type == "text":
            reply_text = bot_service.handle_message(
                message_event.user_id, 
                message_event.content
            )
        elif message_event.message_type == "image":
            reply_text = bot_service.handle_image(
                message_event.user_id,
                message_event.content
            )

        bot_service.messaging_adapter.send_message(
            message_event.reply_token,
            reply_text
        )
        results.append({"event_id": event.webhookEventId, "processed": True})
    
    return {"status": "ok", "processed_events": results}