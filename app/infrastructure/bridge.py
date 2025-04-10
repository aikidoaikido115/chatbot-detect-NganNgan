from app.domain.bridge.interfaces import ConnectLine2DatabaseInterface
import requests
from typing import Optional


class ConnectLine2DatabaseAdapter(ConnectLine2DatabaseInterface):
    def post_requests_users(self, id:str) -> Optional[dict]:
        print("เข้ามาใน POST ได้")
        try:
            url = f"http://127.0.0.1:8000/users?id={id}" # น่าจะต้องเป็น ngrok url
            print(f"URL: {url}")
            response = requests.post(url, timeout=1) # ยิงติดแต่มันค้างต้องรอ timeout
            # response.raise_for_status()  # เช็คว่า response status เป็น 200-299
            print(response.json()) #ลองเช็คว่า close database ถูกต้องไหม async ไหม ทำไมถึงค้าง
            print("สำเร็จ") # ยังไม่ขึ้นตรงนี้ เพราะมันเด้งไป ecxept time out
            return response.json()
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Response: {response.text}")
            return {"HTTP_err":http_err, "Response": response.text}
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error: {conn_err}")
            return {"connection_err": conn_err}
        except requests.exceptions.Timeout as timeout_err:
            print(f"Request timed out: {timeout_err}")
            return{"time out err": timeout_err}
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return {"req_err": req_err}