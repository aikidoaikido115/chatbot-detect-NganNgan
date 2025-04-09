from abc import ABC, abstractmethod


class ConnectLine2DatabaseInterface(ABC):
    @abstractmethod
    def post_requests_users(self, id:str):
        pass

    # @abstractmethod
    # def get_requests_all_users(self) -> str:
    #     pass

    # @abstractmethod
    # def post_requests_command(self, id: int, user_id: str):
    #     pass
    
    # @abstractmethod
    # def get_requests_all_command(self) -> str:
    #     pass
