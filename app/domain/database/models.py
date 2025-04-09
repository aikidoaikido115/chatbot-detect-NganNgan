from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True) # ให้ pk เป็น str โดยดึงมาจากบอทไลน์ และไม่ auto-increment
    def to_dict(self):
        return {
            "id": self.id,
        }

class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String)

    user = relationship("User", back_populates="commands")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name
        }