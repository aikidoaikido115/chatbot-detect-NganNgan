from abc import ABC, abstractmethod
from typing import List
from app.domain.database.models import (
    User,
    Command
)

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
    
    @abstractmethod 
    async def find_by_id(self, id: str) -> User:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    # @abstractmethod
    # async def get_by_id(self, id: str) -> User:
    #     pass

class CommandRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, command: Command) -> Command:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Command:
        pass

    @abstractmethod
    async def get_all(self) -> List[Command]:
        pass
    async def delete_all_user_command(self, user_id: str) -> List[Command]:
        pass

    # @abstractmethod
    # async def get_by_user_id(self, id: str) -> Command:
    #     pass