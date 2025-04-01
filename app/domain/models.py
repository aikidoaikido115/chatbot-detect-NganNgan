from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any


class LineMessageContent(BaseModel):
    id: str
    type: str
    text: Optional[str] = None


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
    message: str
    
    @classmethod
    def from_webhook_event(cls, event: LineEventObject) -> Optional['LineMessageEvent']:
        """สร้าง LineMessageEvent จาก LineEventObject"""
        if event.type != "message" or not event.message or event.message.type != "text":
            return None
            
        user_id = event.source.userId
        if not user_id:
            return None
            
        return cls(
            reply_token=event.replyToken,
            user_id=user_id,
            message=event.message.text or ""
        )