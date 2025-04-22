from app.domain.line.interfaces import LineMessagingInterface
# import requests
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
# print(f"อ่านไหม {LINE_ACCESS_TOKEN}")

class LineMessagingAdapter(LineMessagingInterface):
    async def send_message(self, reply_token: str, message: str):
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
        async with httpx.AsyncClient() as client:
            # ใช้ POST method และส่ง payload ที่ถูกต้อง
            await client.post(url, headers=headers,json=payload)
        # requests.post(url, json=payload, headers=headers)

    async def send_flex(self, reply_token: str, flex_message: dict):
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
                "altText": "แง้นๆๆ",
                "contents": flex_message
            }]
        }
        async with httpx.AsyncClient() as client:
            await client.post(url, headers=headers, json=payload)

        # requests.post(url, json=payload, headers=headers)
    
    async def get_image_content(self, message_id: str) -> bytes:
        url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
        headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
        
        try:
            async with httpx.AsyncClient() as client:
                # ใช้ stream=True สำหรับการดาวน์โหลดไฟล์ขนาดใหญ่
                async with client.stream("GET", url, headers=headers) as response:
                    response.raise_for_status()
                    
                    # เก็บข้อมูลเป็น chunks เพื่อประหยัด memory
                    chunks = []
                    async for chunk in response.aiter_bytes():
                        chunks.append(chunk)
                        
                    return b"".join(chunks)
                    
        except httpx.HTTPStatusError as e:
            print(f"Image Download Error ({e.response.status_code}): {e.response.text}")
            raise
        except Exception as e:
            print(f"Unexpected error in get_image_content: {str(e)}")
            raise