from sqlalchemy.orm import Session
from app.domain.database.models import User, Command
from typing import List
from app.domain.database.interfaces import UserRepositoryInterface, CommandRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def find_by_id(self, id: str) -> User:
        return self.db.query(User).filter(User.id == id).first()

    def get_all(self) -> List[User]:
        return self.db.query(User).all()
    
class CommandRepository(CommandRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, command: Command) -> Command:
        try:
            self.db.add(command)
            self.db.commit()
            self.db.refresh(command)
            return command
        except Exception as e:
            self.db.rollback()
            raise e
        
    def find_by_user_id(self, user_id: str) -> Command:
        return self.db.query(Command).filter(Command.user_id == user_id).first()
    
    def get_all(self) -> List[Command]:
        return self.db.query(Command).all()