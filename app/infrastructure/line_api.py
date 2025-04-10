from app.domain.line.interfaces import LineMessagingInterface
import requests
import os
from dotenv import load_dotenv

load_dotenv()
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
# print(f"อ่านไหม {LINE_ACCESS_TOKEN}")

class LineMessagingAdapter(LineMessagingInterface):
    def send_message(self, reply_token: str, message: str):
        # print("ก่อนส่งข้อความ ธรรมดาๆ")
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

    def send_flex(self, reply_token: str, flex_message: dict):
        # print("ก่อนจะส่ง flex")
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
        }
        payload = {
            "replyToken": reply_token,
            "messages": [{
                "type": "flex",
                "altText": "เทคนิคอะไรดี?",
                "contents": flex_message
            }]
        }
        requests.post(url, json=payload, headers=headers)

    def get_image_content(self, message_id: str) -> bytes:

        print(f"จาก line_api {message_id}")
        url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
        headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
        
        try:
            response = requests.get(url, headers=headers)
            print(f"Response Status: {response.status_code}")  # Debug status
            print(f"Response Headers: {response.headers}")      # Debug headers
            response.raise_for_status()

        except requests.HTTPError as e:
            print(f"HTTP Error Details: {e.response.text}")  # แสดงข้อความ error จาก LINE
            raise
        return response.content