from app.domain.interfaces import LineMessagingInterface
import requests
import os

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")

class LineMessagingAdapter(LineMessagingInterface):
    def send_message(self, reply_token: str, message: str):
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
        }
        payload = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": message}]
        }
        requests.post(url, json=payload, headers=headers)
