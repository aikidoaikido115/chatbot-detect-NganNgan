from abc import ABC, abstractmethod
from typing import Optional

class ConnectLine2DatabaseInterface(ABC):
    @abstractmethod
    async def post_requests_users(self, id:str) -> Optional[dict]:
        pass

    # @abstractmethod
    # def get_requests_all_users(self) -> str: # เอาเป็น get user by id แทน
    #     pass

    # @abstractmethod
    # def post_requests_command(self, id: int, user_id: str):
    #     pass
    
    # @abstractmethod
    # def get_requests_all_command(self) -> str:
    #     pass
