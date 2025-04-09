from app.domain.bridge.interfaces import ConnectLine2DatabaseInterface
import requests


class ConnectLine2DatabaseAdapter(ConnectLine2DatabaseInterface):
    def post_requests_users(self, id:str):
        url = f"http://localhost:8000/users?id={id}"
        requests.post(url)