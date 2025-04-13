from app.domain.bridge.interfaces import ConnectLine2DatabaseInterface
# import requests
import httpx
from typing import Optional


class ConnectLine2DatabaseAdapter(ConnectLine2DatabaseInterface):
    async def post_requests_users(self, id:str) -> Optional[dict]:
        print("เข้ามาใน users POST ได้")
        try:
            url = f"http://127.0.0.1:8000/users?id={id}"
            print(f"URL: {url}")
            async with httpx.AsyncClient(timeout=2) as client:
                response = await client.post(url)
                response.raise_for_status()
                print("post user สำเร็จ")
                return response.json()
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None
    
    async def post_requests_command(self, user_id: str, name: str) -> Optional[dict]:
        print("เข้ามาใน command POST ได้")
        try:
            url = f"http://127.0.0.1:8000/commands?user_id={user_id}&name={name}"
            print(f"URL: {url}")
            async with httpx.AsyncClient(timeout=2) as client:
                response = await client.post(url)
                response.raise_for_status()
                print("post command สำเร็จ")
                return response.json()
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None
    
    async def get_requests_command_by_user_id(self, user_id: str) -> Optional[dict]:
        print("เข้ามาใน command GET ได้")
        try:
            url = f"http://127.0.0.1:8000/command?user_id={user_id}"
            print(f"URL: {url}")
            async with httpx.AsyncClient(timeout=2) as client:
                response = await client.get(url)
                response.raise_for_status()
                print("get command สำเร็จ")
                return response.json()
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None