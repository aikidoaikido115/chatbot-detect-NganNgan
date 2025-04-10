from fastapi import APIRouter, Depends, HTTPException
from app.application.services import LineBotService
from app.domain.line.interfaces import LineBotServiceInterface
from app.domain.line.models import LineWebhookRequest, LineMessageEvent
from app.infrastructure.line_api import LineMessagingAdapter
from app.infrastructure.file_storage import ImageStorageAdapter
from app.infrastructure.ocr_api import OcrAdapter
from app.infrastructure.image_enhance import ImageEnhanceAdapter

from app.infrastructure.database.postgres import get_db
from app.infrastructure.database.repositories import UserRepository, CommandRepository
from app.application.services import UserService, CommandService
from app.domain.database.models import User, Command
from typing import List, Dict, Any

# from app.domain.bridge.interfaces import ConnectLine2DatabaseInterface
from app.infrastructure.bridge import ConnectLine2DatabaseAdapter

router = APIRouter()



@router.get("/")
async def hello():
    return {"message":"Welcome to Chatbot"}


@router.post("/users")
async def create_user(id: str, db=Depends(get_db)):
    try:
        repo = UserRepository(db)
        service = UserService(repo)
        return await service.create_user(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_users(db=Depends(get_db)):
    try:
        repo = UserRepository(db)
        service = UserService(repo)
        users = await service.get_users()
        return [user.to_dict() for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/commands")
async def create_command(id: int, user_id: str, db=Depends(get_db)):
    try:
        repo = CommandRepository(db)
        service = CommandService(repo)
        return await service.create_command(id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/commands", response_model=List[Dict[str, Any]])
async def get_commands(db=Depends(get_db)):
    try:
        repo = CommandRepository(db)
        service = CommandService(repo)
        commands = await service.get_commands()
        return [command.to_dict() for command in commands]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_line_bot_service() -> LineBotServiceInterface:
    messaging_adapter = LineMessagingAdapter()
    image_storage = ImageStorageAdapter()
    ocr = OcrAdapter()
    enhance = ImageEnhanceAdapter()
    bridge = ConnectLine2DatabaseAdapter()
    return LineBotService(messaging_adapter, image_storage, ocr, enhance, bridge)

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

        # print(f"tpye ของ reply_text {type(reply_text)}")
        if isinstance(reply_text, str):
            bot_service.messaging_adapter.send_message(
                message_event.reply_token,
                reply_text
            )
        else:
            bot_service.messaging_adapter.send_flex(
                message_event.reply_token,
                reply_text
            )
        results.append({"event_id": event.webhookEventId, "processed": True})
    
    return {"status": "ok", "processed_events": results}