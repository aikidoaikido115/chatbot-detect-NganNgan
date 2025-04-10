from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.database.models import User, Command
from typing import List
from app.domain.database.interfaces import UserRepositoryInterface, CommandRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            raise e

    async def find_by_id(self, id: str) -> User:
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first()

    async def get_all(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()
    
class CommandRepository(CommandRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, command: Command) -> Command:
        try:
            self.db.add(command)
            await self.db.commit()
            await self.db.refresh(command)
            return command
        except Exception as e:
            await self.db.rollback()
            raise e
        
    async def find_by_user_id(self, user_id: str) -> Command:
        result = await self.db.execute(select(Command).filter(Command.id == user_id))
        return result.scalars().first()
    
    async def get_all(self) -> List[Command]:
        result = await self.db.execute(select(Command))
        return result.scalars().all()