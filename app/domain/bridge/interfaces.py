from abc import ABC, abstractmethod
from typing import Optional

class ConnectLine2DatabaseInterface(ABC):
    @abstractmethod
    async def post_requests_users(self, id: str) -> Optional[dict]:
        pass

    # @abstractmethod
    # def get_requests_users_by_id(self) -> str:
    #     pass

    @abstractmethod
    def post_requests_command(self, user_id: str, name: str):
        pass
    
    @abstractmethod
    def get_requests_command_by_user_id(self, user_id: str) -> str:
        pass
