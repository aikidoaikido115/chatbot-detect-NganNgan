from fastapi import APIRouter, Depends
from app.application.services import LineBotService
from app.domain.interfaces import LineBotServiceInterface
from app.domain.models import LineWebhookRequest, LineMessageEvent
from app.infrastructure.line_api import LineMessagingAdapter

router = APIRouter()

def get_line_bot_service() -> LineBotServiceInterface:
    messaging_adapter = LineMessagingAdapter()
    return LineBotService(messaging_adapter)

@router.post("/webhook")
async def line_webhook(webhook: LineWebhookRequest, bot_service: LineBotServiceInterface = Depends(get_line_bot_service)):
    results = []
    for event in webhook.events:
        message_event = LineMessageEvent.from_webhook_event(event)
        if message_event:
            reply_text = bot_service.handle_message(message_event.user_id, message_event.message)
            bot_service.messaging_adapter.send_message(message_event.reply_token, reply_text)
            results.append({"event_id": event.webhookEventId, "processed": True})
        else:
            results.append({"event_id": event.webhookEventId, "processed": False})
    
    return {"status": "ok", "processed_events": results}