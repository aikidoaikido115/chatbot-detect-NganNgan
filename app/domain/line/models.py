from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

class ImageContent(BaseModel):
    originalContentUrl: str
    previewImageUrl: str

class LineMessageContent(BaseModel):
    id: str
    type: str
    text: Optional[str] = None
    image: Optional[ImageContent] = None


class LineSource(BaseModel):
    type: Literal["user", "group", "room"]
    userId: Optional[str] = None
    groupId: Optional[str] = None
    roomId: Optional[str] = None


class LineEventObject(BaseModel):
    type: Literal["message", "follow", "unfollow", "join", "leave", "postback", "beacon", "accountLink", "memberJoined", "memberLeft"]
    replyToken: Optional[str] = None
    source: LineSource
    timestamp: int
    mode: str
    webhookEventId: str
    deliveryContext: Dict[str, bool]
    message: Optional[LineMessageContent] = None
    postback: Optional[Dict[str, Any]] = None  # เพิ่มฟิลด์อื่นๆ ตามความต้องการ


class LineWebhookRequest(BaseModel):
    destination: str
    events: List[LineEventObject]


# Class สำหรับ parsing webhook data และใช้ใน app
class LineMessageEvent(BaseModel):
    reply_token: str
    user_id: str
    message_type: Literal["text", "image"]
    content: str
    
    @classmethod
    def from_webhook_event(cls, event: LineEventObject) -> Optional['LineMessageEvent']:
        
        print(event)
        if event.type != "message" or not event.message:
            return None
            
        user_id = event.source.userId
        if not user_id:
            return None
        

        if event.message.type not in ["text", "image"]:
            return None

        # print(event.message.type + "อะไรวะ")
        content = (
            event.message.text 
            if event.message.type == "text" 
            else event.message.id
        )

        return cls(
            reply_token=event.replyToken,
            user_id=user_id,
            message_type=event.message.type,
            content=content
        )